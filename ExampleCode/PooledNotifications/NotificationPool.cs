using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Pool;

namespace UnityBestPractices.Samples.Pooling
{
    /// <summary>Main-thread owner of both borrowed and retained items. Capacity limits retained items only.</summary>
    public sealed class NotificationPool : IDisposable
    {
        private readonly ObjectPool<PooledNotification> m_pool;
        private readonly Dictionary<PooledNotification, NotificationLease> m_leases =
            new Dictionary<PooledNotification, NotificationLease>();
        private readonly NotificationSignals m_signals;
        private readonly INotificationDelay m_delay;
        private bool m_isDisposed;

        public int BorrowedCount => m_leases.Count;

        public NotificationPool(Func<PooledNotification> createItem, NotificationSignals signals,
            INotificationDelay delay, int retainedCapacity = 4)
        {
            if (createItem == null || signals == null || delay == null || retainedCapacity < 1)
            {
                throw new ArgumentException("Supply an inactive-item factory, signals, delay, and positive capacity.");
            }
            m_signals = signals;
            m_delay = delay;
            m_pool = new ObjectPool<PooledNotification>(createItem, null, null, DestroyItem,
                collectionCheck: true, defaultCapacity: retainedCapacity, maxSize: retainedCapacity);
        }

        /// <summary>Initializes state and subscriptions before handing out a unique checkout.</summary>
        public NotificationLease Acquire(string message)
        {
            if (m_isDisposed)
            {
                throw new ObjectDisposedException(nameof(NotificationPool));
            }
            PooledNotification item = m_pool.Get();
            if (item == null || item.gameObject.activeSelf)
            {
                if (item != null)
                {
                    DestroyItem(item);
                }
                throw new InvalidOperationException("The factory must create a live, inactive item.");
            }
            NotificationLease lease = new NotificationLease(this, item, m_delay);
            m_leases.Add(item, lease);
            item.BeginLease(message, m_signals);
            return lease;
        }

        /// <summary>Ends every lease, then destroys retained objects. Later acquisition is rejected.</summary>
        public void Dispose()
        {
            if (m_isDisposed)
            {
                return;
            }
            m_isDisposed = true;
            List<NotificationLease> leases = new List<NotificationLease>(m_leases.Values);
            foreach (NotificationLease lease in leases)
            {
                lease.Dispose();
            }
            m_pool.Clear();
        }

        internal void Return(NotificationLease lease)
        {
            PooledNotification item = lease.Item;
            if (!m_leases.TryGetValue(item, out NotificationLease current) || current != lease)
            {
                return;
            }
            m_leases.Remove(item);
            item.EndLease();
            m_pool.Release(item);
        }

        private static void DestroyItem(PooledNotification item)
        {
            if (Application.isPlaying)
            {
                UnityEngine.Object.Destroy(item.gameObject);
            }
            else
            {
                UnityEngine.Object.DestroyImmediate(item.gameObject);
            }
        }
    }
}
