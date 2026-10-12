using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.UIElements;

#if UNITY_EDITOR
using UnityEditor;
#endif

namespace UnityBestPractices.Samples.Tests
{
    public sealed class SampleViewLifecycleTests
    {
        private GameObject m_host;
        private PanelSettings m_panel;

        [UnityTearDown]
        public IEnumerator TearDown()
        {
            if (m_host != null) Object.Destroy(m_host);
            if (m_panel != null) Object.Destroy(m_panel);
            yield return null;
        }

        [UnityTest]
        public IEnumerator ReenableViewAndDocument_PreservesCount_AndBindsOnce()
        {
#if UNITY_EDITOR
            string[] guids = AssetDatabase.FindAssets("SampleView t:VisualTreeAsset");
            Assert.That(guids.Length, Is.EqualTo(1), "Install one copy of the sample UXML.");
            var tree = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>(AssetDatabase.GUIDToAssetPath(guids[0]));
            m_host = new GameObject("Counter lifecycle fixture");
            m_host.SetActive(false);
            m_panel = ScriptableObject.CreateInstance<PanelSettings>();
            var document = m_host.AddComponent<UIDocument>();
            document.panelSettings = m_panel;
            document.visualTreeAsset = tree;
            var view = m_host.AddComponent<SampleView>();
            m_host.SetActive(true);
            yield return null;

            Button oldButton = document.rootVisualElement.Q<Button>("counter__increment-button");
            Click(oldButton);
            Click(oldButton);
            Assert.That(view.Count, Is.EqualTo(2));
            view.enabled = false;
            Click(oldButton);
            Assert.That(view.Count, Is.EqualTo(2), "Disabled presentation must stop reacting.");
            view.enabled = true;
            yield return null;
            Assert.That(document.rootVisualElement.Q<Label>("counter__count").text, Is.EqualTo("2"));
            Click(oldButton);
            Assert.That(view.Count, Is.EqualTo(3));

            document.enabled = false;
            yield return null;
            Click(oldButton);
            Assert.That(view.Count, Is.EqualTo(3), "Detached tree must stop reacting.");
            document.enabled = true;
            yield return null;
            yield return null;
            Assert.That(document.rootVisualElement.Q<Label>("counter__count").text, Is.EqualTo("3"));
            Click(document.rootVisualElement.Q<Button>("counter__increment-button"));
            Assert.That(view.Count, Is.EqualTo(4), "Rebinding must not duplicate subscriptions.");
#else
            Assert.Ignore("Editor integration fixture uses AssetDatabase; player fixture is not supplied.");
            yield break;
#endif
        }

        private static void Click(Button button)
        {
            Assert.That(button, Is.Not.Null);
            using (NavigationSubmitEvent evt = NavigationSubmitEvent.GetPooled())
            {
                evt.target = button;
                button.SendEvent(evt);
            }
        }
    }
}
