using UnityEngine;

namespace UnityBestPractices.Samples.Pooling
{
    /// <summary>Minimal notification state. Visual rendering is deliberately outside this example.</summary>
    public sealed class PooledNotification : MonoBehaviour
    {
        private NotificationSignals m_signals;

        public string Message { get; private set; } = string.Empty;
        public int PulseCount { get; private set; }

        internal void BeginLease(string message, NotificationSignals signals)
        {
            Message = message;
            PulseCount = 0;
            m_signals = signals;
            m_signals.Pulsed += HandlePulsed;
            gameObject.SetActive(true);
        }

        internal void EndLease()
        {
            if (m_signals != null)
            {
                m_signals.Pulsed -= HandlePulsed;
                m_signals = null;
            }
            Message = string.Empty;
            PulseCount = 0;
            gameObject.SetActive(false);
        }

        private void HandlePulsed()
        {
            PulseCount++;
        }
    }
}
