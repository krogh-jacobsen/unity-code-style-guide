using System.Threading;
using UnityEngine;

namespace UnityBestPractices.Samples.Cancellation
{
    /// <summary>Local preview provider; replace with the project's actual data service.</summary>
    public sealed class DelayedSearchService : ISearchService
    {
        private readonly float m_delayInSeconds;

        public DelayedSearchService(float delayInSeconds)
        {
            m_delayInSeconds = Mathf.Max(0f, delayInSeconds);
        }

        public async Awaitable<string> SearchAsync(string query, CancellationToken cancellationToken)
        {
            await Awaitable.WaitForSecondsAsync(m_delayInSeconds, cancellationToken);
            return $"Preview: {query}";
        }
    }
}
