using System;
using System.Threading;
using System.Threading.Tasks;
using NUnit.Framework;
using UnityEngine;

namespace UnityBestPractices.Samples.Pooling.Tests
{
    public sealed class NotificationPoolTests
    {
        [Test]
        public async Task OldTimerAndDuplicateReturn_CannotReturnTheReusedItem()
        {
            NotificationSignals signals = new NotificationSignals();
            ControlledDelay delay = new ControlledDelay();
            using (NotificationPool pool = new NotificationPool(CreateItem, signals, delay))
            {
                NotificationLease first = pool.Acquire("first");
                PooledNotification item = first.Item;
                Awaitable timer = first.ReturnAfterAsync(1f);
                signals.Pulse();
                Assert.That(item.PulseCount, Is.EqualTo(1));
                first.Dispose();
                Assert.That(delay.Token.IsCancellationRequested, Is.True);
                signals.Pulse();
                Assert.That(item.PulseCount, Is.Zero, "Returned items unsubscribe and reset.");
                NotificationLease second = pool.Acquire("second");
                Assert.That(second.Item, Is.SameAs(item));
                first.Dispose();
                delay.Completion.SetResult();
                await timer;
                Assert.That(second.IsReturned, Is.False);
                Assert.That(pool.BorrowedCount, Is.EqualTo(1));
                Assert.That(item.Message, Is.EqualTo("second"));
                signals.Pulse();
                Assert.That(item.PulseCount, Is.EqualTo(1), "Reuse subscribes exactly once.");
                second.Dispose();
            }
        }

        [Test]
        public async Task DisposeOwner_CancelsWorkAndDestroysBorrowedAndRetainedItems()
        {
            NotificationSignals signals = new NotificationSignals();
            ControlledDelay delay = new ControlledDelay();
            NotificationPool pool = new NotificationPool(CreateItem, signals, delay, retainedCapacity: 1);
            NotificationLease borrowed = pool.Acquire("borrowed");
            NotificationLease returned = pool.Acquire("returned");
            PooledNotification borrowedItem = borrowed.Item;
            PooledNotification returnedItem = returned.Item;
            returned.Dispose();
            Awaitable timer = borrowed.ReturnAfterAsync(1f);
            pool.Dispose();
            pool.Dispose();
            Assert.That(delay.Token.IsCancellationRequested, Is.True);
            delay.Completion.SetResult();
            await timer;
            signals.Pulse();
            Assert.That(borrowedItem == null, Is.True);
            Assert.That(returnedItem == null, Is.True);
            Assert.That(pool.BorrowedCount, Is.Zero);
            Assert.Throws<ObjectDisposedException>(() => pool.Acquire("late"));
        }

        private static PooledNotification CreateItem()
        {
            GameObject item = new GameObject("Notification fixture");
            item.SetActive(false);
            return item.AddComponent<PooledNotification>();
        }

        private sealed class ControlledDelay : INotificationDelay
        {
            public AwaitableCompletionSource Completion { get; } = new AwaitableCompletionSource();
            public CancellationToken Token { get; private set; }

            public Awaitable WaitAsync(float delayInSeconds, CancellationToken cancellationToken)
            {
                Token = cancellationToken;
                // Deliberately ignore cancellation; the lease identity must still protect reuse.
                return Completion.Awaitable;
            }
        }
    }
}
