using UnityEngine;
using UnityEngine.UIElements;

namespace UnityStarter.SceneTemplates
{
    /// <summary>Demonstrates scene-local UI selection and modal focus without a game session.</summary>
    [RequireComponent(typeof(UIDocument))]
    public sealed class PreviewScreen : MonoBehaviour
    {
        private const string k_hiddenClass = "is-hidden";
        private VisualElement m_root;
        private VisualElement m_modal;
        private Button m_openButton;
        private Button m_closeButton;
        private Button m_selectButton;
        private Label m_status;
        private VisualElement m_workspace;

        private void OnEnable()
        {
            m_root = GetComponent<UIDocument>().rootVisualElement;
            m_modal = m_root.Q("modalOverlay");
            m_workspace = m_root.Q("workspace");
            m_openButton = m_root.Q<Button>("openModal");
            m_closeButton = m_root.Q<Button>("closeModal");
            m_selectButton = m_root.Q<Button>("selectItem");
            m_status = m_root.Q<Label>("status");
            m_openButton.clicked += OpenModal;
            m_closeButton.clicked += CloseModal;
            m_selectButton.clicked += SelectItem;
            m_root.RegisterCallback<KeyDownEvent>(HandleKeyDown, TrickleDown.TrickleDown);
            CloseModal();
        }

        private void OnDisable()
        {
            m_openButton.clicked -= OpenModal;
            m_closeButton.clicked -= CloseModal;
            m_selectButton.clicked -= SelectItem;
            m_root.UnregisterCallback<KeyDownEvent>(HandleKeyDown, TrickleDown.TrickleDown);
        }

        private void OpenModal()
        {
            m_workspace.SetEnabled(false);
            m_modal.RemoveFromClassList(k_hiddenClass);
            m_closeButton.Focus();
        }

        private void CloseModal()
        {
            m_modal.AddToClassList(k_hiddenClass);
            m_workspace.SetEnabled(true);
            m_openButton.Focus();
        }

        private void SelectItem()
        {
            m_status.text = "Selected: Workshop / production building";
        }

        private void HandleKeyDown(KeyDownEvent evt)
        {
            if (evt.keyCode == KeyCode.Escape && !m_modal.ClassListContains(k_hiddenClass))
            {
                CloseModal();
                evt.StopPropagation();
            }
        }
    }
}
