using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace UnityBestPractices.Samples.Cancellation.Tests
{
    public sealed class SearchScreenTests
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
        public IEnumerator DisableAndReopen_RendersOnlyTheNewSessionResult()
        {
            m_host = new GameObject("Search screen fixture");
            SearchScreenExample screen = m_host.AddComponent<SearchScreenExample>();
            screen.RequestSearch("old");
            screen.enabled = false;
            screen.enabled = true;
            screen.RequestSearch("new");
            float deadline = Time.realtimeSinceStartup + 5f;
            while (screen.DisplayedResult == string.Empty && Time.realtimeSinceStartup < deadline)
            {
                yield return null;
            }
            Assert.That(screen.DisplayedResult, Is.EqualTo("Preview: new"));
            screen.RequestSearch("destroyed");
            Object.Destroy(m_host);
            yield return null;
            yield return new WaitForSeconds(0.3f);
        }
    }
}
