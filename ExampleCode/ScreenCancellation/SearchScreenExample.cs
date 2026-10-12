using System;
using UnityEngine;

namespace UnityBestPractices.Samples.Cancellation
{
    /// <summary>A screen-lifetime adapter; connect UI input to RequestSearch and render DisplayedResult.</summary>
    public sealed class SearchScreenExample : MonoBehaviour
    {
        [SerializeField, Tooltip("Query used by the context-menu preview.")]
        private string m_query = "Railroad";
        [SerializeField, Min(0f), Tooltip("Simulated request duration in seconds.")]
        private float m_delayInSeconds = 0.25f;
        private SearchSession m_session;

        public string DisplayedResult { get; private set; } = string.Empty;

        private void OnEnable()
        {
            DisplayedResult = string.Empty;
            m_session = new SearchSession(new DelayedSearchService(m_delayInSeconds));
            m_session.ResultChanged += HandleResultChanged;
        }

        private void OnDisable()
        {
            m_session.ResultChanged -= HandleResultChanged;
            m_session.Dispose();
            m_session = null;
        }

        /// <summary>Starts an observed request for the current screen session.</summary>
        public async void RequestSearch(string query)
        {
            SearchSession session = m_session;
            if (session == null)
            {
                return;
            }

            try
            {
                await session.SearchAsync(query);
            }
            catch (Exception exception)
            {
                // UI callbacks cannot return an Awaitable; this boundary observes every failure.
                Debug.LogException(exception, this);
            }
        }

        [ContextMenu("Request Preview")]
        private void RequestPreview()
        {
            RequestSearch(m_query);
        }

        private void HandleResultChanged(string result)
        {
            DisplayedResult = result;
        }
    }
}
