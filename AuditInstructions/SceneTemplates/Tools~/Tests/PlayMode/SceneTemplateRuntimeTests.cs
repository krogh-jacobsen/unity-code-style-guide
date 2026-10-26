using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;
using UnityEngine.UIElements;

namespace UnityStarter.SceneTemplates.Tests
{
    /// <summary>Exercises actual input, scene lifetimes, and modal behavior in the disposable consumer.</summary>
    public sealed class SceneTemplateRuntimeTests
    {
        private Keyboard m_keyboard;
        private InputSettings.BackgroundBehavior m_previousBackgroundBehavior;
        private InputSettings.EditorInputBehaviorInPlayMode m_previousEditorBehavior;

        [SetUp]
        public void SetUp()
        {
            // A batch Editor has no focused Game view; restore both temporary choices in teardown.
            m_previousBackgroundBehavior = InputSystem.settings.backgroundBehavior;
            m_previousEditorBehavior = InputSystem.settings.editorInputBehaviorInPlayMode;
            InputSystem.settings.backgroundBehavior = InputSettings.BackgroundBehavior.IgnoreFocus;
            InputSystem.settings.editorInputBehaviorInPlayMode = InputSettings.EditorInputBehaviorInPlayMode.AllDeviceInputAlwaysGoesToGameView;
        }

        [UnityTearDown]
        public IEnumerator TearDown()
        {
            if (m_keyboard != null)
            {
                InputSystem.RemoveDevice(m_keyboard);
                m_keyboard = null;
            }

            InputSystem.settings.backgroundBehavior = m_previousBackgroundBehavior;
            InputSystem.settings.editorInputBehaviorInPlayMode = m_previousEditorBehavior;

            yield return SceneManager.LoadSceneAsync("Assets/Generated/UIPreview0.unity");
        }

        [UnityTest]
        public IEnumerator CameraReadsInputBlocksNavigationAndKeepsInputInstancesIndependent()
        {
            yield return SceneManager.LoadSceneAsync("Assets/Generated/StrategySandbox0.unity");
            var controller = Object.FindAnyObjectByType<StrategyCameraController>();
            var second = Object.Instantiate(controller.gameObject);
            second.SetActive(false);
            controller.SendMessage("OnApplicationFocus", true);
            m_keyboard = InputSystem.AddDevice<Keyboard>();
            Vector3 before = controller.transform.position;
            InputSystem.QueueStateEvent(m_keyboard, new KeyboardState(Key.W));
            yield return new WaitForSecondsRealtime(0.2f);

            Assert.That(Vector3.Distance(before, controller.transform.position), Is.GreaterThan(0.01f));
            controller.SetInputBlocked(true);
            Vector3 blocked = controller.transform.position;
            yield return new WaitForSecondsRealtime(0.1f);

            Assert.That(Vector3.Distance(blocked, controller.transform.position), Is.LessThan(0.001f));
            controller.SetOrthographic(true);
            Assert.That(controller.GetComponentInChildren<Camera>().orthographic, Is.True);
            controller.SetInputBlocked(false);
            controller.enabled = false;
            controller.enabled = true;
            yield return null;
            Object.Destroy(second);
            InputSystem.QueueStateEvent(m_keyboard, new KeyboardState());
            yield return null;
        }

        [UnityTest]
        public IEnumerator PreviewSelectionModalAndHostReenableRestoreFocus()
        {
            yield return SceneManager.LoadSceneAsync("Assets/Generated/UIPreview0.unity");
            var screen = Object.FindAnyObjectByType<PreviewScreen>();
            screen.gameObject.SetActive(false);
            yield return null;
            screen.gameObject.SetActive(true);
            yield return null;
            var root = screen.GetComponent<UIDocument>().rootVisualElement;
            var open = root.Q<Button>("openModal");
            var close = root.Q<Button>("closeModal");
            using (var evt = NavigationSubmitEvent.GetPooled())
            {
                evt.target = root.Q<Button>("selectItem");
                root.Q<Button>("selectItem").SendEvent(evt);
            }

            Assert.That(root.Q<Label>("status").text, Does.StartWith("Selected: Workshop"));
            using (var evt = NavigationSubmitEvent.GetPooled())
            {
                evt.target = open;
                open.SendEvent(evt);
            }

            Assert.That(root.Q("modalOverlay").ClassListContains("is-hidden"), Is.False);
            Assert.That(root.Q("workspace").enabledSelf, Is.False);
            Assert.That(root.focusController.focusedElement, Is.SameAs(close));
            using (var evt = NavigationSubmitEvent.GetPooled())
            {
                evt.target = close;
                close.SendEvent(evt);
            }

            Assert.That(root.Q("modalOverlay").ClassListContains("is-hidden"), Is.True);
            Assert.That(root.Q("workspace").enabledSelf, Is.True);
            Assert.That(root.focusController.focusedElement, Is.SameAs(open));
            Assert.That(root.Q<ScrollView>("catalogue").contentContainer.childCount, Is.EqualTo(8));
            using (var evt = NavigationSubmitEvent.GetPooled())
            {
                evt.target = open;
                open.SendEvent(evt);
            }

            using (var evt = KeyDownEvent.GetPooled(new Event { type = EventType.KeyDown, keyCode = KeyCode.Escape }))
            {
                evt.target = close;
                close.SendEvent(evt);
            }

            Assert.That(root.Q("modalOverlay").ClassListContains("is-hidden"), Is.True);
            Assert.That(root.focusController.focusedElement, Is.SameAs(open));
        }
    }
}
