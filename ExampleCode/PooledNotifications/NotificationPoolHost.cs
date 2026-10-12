using System;
using UnityEngine;

namespace UnityBestPractices.Samples.Pooling
{
    /// <summary>Object-lifetime owner of a notification pool. Attach to an active object to preview.</summary>
    public sealed class NotificationPoolHost : MonoBehaviour
    {
        [SerializeField, Min(0f), Tooltip("Preview notification lease duration in seconds.")]
        private float m_durationInSeconds = 1f;
        private readonly NotificationSignals m_signals = new NotificationSignals();
        private NotificationPool m_pool;

        public NotificationPool Pool => m_pool;

        private void Awake()
        {
            m_pool = new NotificationPool(CreateItem, m_signals, new NotificationDelay());
        }

        private void OnDestroy()
        {
            m_pool?.Dispose();
        }

        /// <summary>Creates a marker and observes its timed return.</summary>
        [ContextMenu("Show Notification")]
        public async void ShowNotification()
        {
            if (!Application.isPlaying || m_pool == null)
            {
                return;
            }
            NotificationLease lease = null;
            try
            {
                lease = m_pool.Acquire("Notification preview");
                await lease.ReturnAfterAsync(m_durationInSeconds);
            }
            catch (Exception exception)
            {
                Debug.LogException(exception, this);
            }
            finally
            {
                lease?.Dispose();
            }
        }

        /// <summary>Sends an instance-owned event to current leases.</summary>
        [ContextMenu("Pulse Notifications")]
        public void PulseNotifications()
        {
            m_signals.Pulse();
        }

        private PooledNotification CreateItem()
        {
            GameObject item = new GameObject("Pooled notification");
            item.SetActive(false);
            item.transform.SetParent(transform, false);
            return item.AddComponent<PooledNotification>();
        }
    }
}
