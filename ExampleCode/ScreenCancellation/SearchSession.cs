using System;
using System.Threading;
using UnityEngine;

namespace UnityBestPractices.Samples.Cancellation
{
    /// <summary>Owns requests for one open screen. Calls and completions belong on the main thread.</summary>
    public sealed class SearchSession : IDisposable
    {
        private readonly ISearchService m_service;
        private CancellationTokenSource m_currentRequest;
        private bool m_isDisposed;

        public string Result { get; private set; } = string.Empty;
        public event Action<string> ResultChanged;

        public SearchSession(ISearchService service)
        {
            m_service = service ?? throw new ArgumentNullException(nameof(service));
        }

        /// <summary>Cancels the previous request and publishes only the current request's result.</summary>
        public async Awaitable SearchAsync(string query)
        {
            if (m_isDisposed)
            {
                throw new ObjectDisposedException(nameof(SearchSession));
            }

            CancellationTokenSource previousRequest = m_currentRequest;
            CancellationTokenSource request = new CancellationTokenSource();
            m_currentRequest = request;
            previousRequest?.Cancel();

            try
            {
                string result = await m_service.SearchAsync(query, request.Token);
                // Cancellation is cooperative: a provider can complete after cancellation.
                if (!m_isDisposed && m_currentRequest == request && !request.IsCancellationRequested)
                {
                    Result = result;
                    ResultChanged?.Invoke(result);
                }
            }
            catch (OperationCanceledException) when (request.IsCancellationRequested)
            {
                // Closing or superseding this request is an expected outcome.
            }
            finally
            {
                if (m_currentRequest == request)
                {
                    m_currentRequest = null;
                }
                // The operation owns disposal; cancellation does not prove the provider has stopped.
                request.Dispose();
            }
        }

        /// <summary>Closes this session. Reopening a screen creates a new session.</summary>
        public void Dispose()
        {
            if (m_isDisposed)
            {
                return;
            }

            m_isDisposed = true;
            CancellationTokenSource request = m_currentRequest;
            m_currentRequest = null;
            ResultChanged = null;
            request?.Cancel();
        }
    }
}
