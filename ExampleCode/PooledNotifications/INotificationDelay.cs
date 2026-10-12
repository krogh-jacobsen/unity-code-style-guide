using System.Threading;
using UnityEngine;

namespace UnityBestPractices.Samples.Pooling
{
    /// <summary>A replaceable clock for deterministic lease-lifetime tests.</summary>
    public interface INotificationDelay
    {
        Awaitable WaitAsync(float delayInSeconds, CancellationToken cancellationToken);
    }

    public sealed class NotificationDelay : INotificationDelay
    {
        public Awaitable WaitAsync(float delayInSeconds, CancellationToken cancellationToken)
        {
            return Awaitable.WaitForSecondsAsync(delayInSeconds, cancellationToken);
        }
    }
}
