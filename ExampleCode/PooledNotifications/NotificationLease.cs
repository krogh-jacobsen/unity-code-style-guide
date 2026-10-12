using System;
using System.Threading;
using UnityEngine;

namespace UnityBestPractices.Samples.Pooling
{
    /// <summary>One checkout identity; a stale lease cannot return a later checkout of the same item.</summary>
    public sealed class NotificationLease : IDisposable
    {
        private readonly NotificationPool m_owner;
        private readonly INotificationDelay m_delay;
        private CancellationTokenSource m_returnRequest;
        private bool m_isDisposed;

        public PooledNotification Item { get; }
        public bool IsReturned => m_isDisposed;

        internal NotificationLease(NotificationPool owner, PooledNotification item, INotificationDelay delay)
        {
            m_owner = owner;
            Item = item;
            m_delay = delay;
        }

        /// <summary>Schedules one return. The caller must await once and observe failures.</summary>
        public async Awaitable ReturnAfterAsync(float delayInSeconds)
        {
            if (m_isDisposed)
            {
                return;
            }
            if (m_returnRequest != null)
            {
                throw new InvalidOperationException("A return is already scheduled for this lease.");
            }

            CancellationTokenSource request = new CancellationTokenSource();
            m_returnRequest = request;
            try
            {
                await m_delay.WaitAsync(delayInSeconds, request.Token);
                // Protect reuse even when a delay provider ignores cancellation.
                if (!m_isDisposed && !request.IsCancellationRequested)
                {
                    Dispose();
                }
            }
            catch (OperationCanceledException) when (request.IsCancellationRequested)
            {
                // Early return or owner teardown ends this lease's timer.
            }
            finally
            {
                m_returnRequest = null;
                request.Dispose();
            }
        }

        /// <summary>Returns this checkout once, cancels its work, and removes its subscriptions.</summary>
        public void Dispose()
        {
            if (m_isDisposed)
            {
                return;
            }
            m_isDisposed = true;
            m_returnRequest?.Cancel();
            m_owner.Return(this);
        }
    }
}
