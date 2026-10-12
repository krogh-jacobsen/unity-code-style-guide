using System;

namespace UnityBestPractices.Samples.Pooling
{
    /// <summary>Instance-owned signal source; no static subscribers survive a Play session.</summary>
    public sealed class NotificationSignals
    {
        public event Action Pulsed;

        /// <summary>Notifies currently leased markers.</summary>
        public void Pulse()
        {
            Pulsed?.Invoke();
        }
    }
}
