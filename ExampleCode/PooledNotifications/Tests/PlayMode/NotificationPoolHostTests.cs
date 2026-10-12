using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace UnityBestPractices.Samples.Pooling.Tests
{
    public sealed class NotificationPoolHostTests
    {
        private GameObject m_host;

        [UnityTearDown]
        public IEnumerator TearDown()
        {
            if (m_host != null)
            {
                Object.Destroy(m_host);
            }
            yield return null;
        }

        [UnityTest]
        public IEnumerator HostDestruction_RemovesBorrowedAndRetainedChildren()
        {
            m_host = new GameObject("Notification pool host fixture");
            NotificationPoolHost host = m_host.AddComponent<NotificationPoolHost>();
            NotificationLease borrowed = host.Pool.Acquire("borrowed");
            NotificationLease retained = host.Pool.Acquire("retained");
            PooledNotification borrowedItem = borrowed.Item;
            PooledNotification retainedItem = retained.Item;
            retained.Dispose();
            host.ShowNotification();
            Object.Destroy(m_host);
            yield return null;
            yield return null;
            Assert.That(borrowed.IsReturned, Is.True);
            Assert.That(borrowedItem == null, Is.True);
            Assert.That(retainedItem == null, Is.True);
        }

        [UnityTest]
        public IEnumerator TimedReturn_MakesTheItemAvailableForReuse()
        {
            m_host = new GameObject("Timed notification fixture");
            NotificationPoolHost host = m_host.AddComponent<NotificationPoolHost>();
            NotificationLease lease = host.Pool.Acquire("timed");
            ObserveReturn(lease);
            float deadline = Time.realtimeSinceStartup + 5f;
            while (!lease.IsReturned && Time.realtimeSinceStartup < deadline)
            {
                yield return null;
            }
            Assert.That(lease.IsReturned, Is.True);
            Assert.That(host.Pool.BorrowedCount, Is.Zero);
            NotificationLease reused = host.Pool.Acquire("reused");
            Assert.That(reused.Item, Is.SameAs(lease.Item));
            reused.Dispose();
        }

        private static async void ObserveReturn(NotificationLease lease)
        {
            try
            {
                await lease.ReturnAfterAsync(0.01f);
            }
            catch (System.Exception exception)
            {
                Debug.LogException(exception);
            }
        }
    }
}
