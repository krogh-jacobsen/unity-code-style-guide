using System.Threading;
using UnityEngine;

namespace UnityBestPractices.Samples.Cancellation
{
    /// <summary>Returns one result per request; callers await each Awaitable once.</summary>
    public interface ISearchService
    {
        Awaitable<string> SearchAsync(string query, CancellationToken cancellationToken);
    }
}
