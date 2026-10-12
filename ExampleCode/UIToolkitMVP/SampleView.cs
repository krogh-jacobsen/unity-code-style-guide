using System;
using UnityEngine;
using UnityEngine.UIElements;

namespace UnityBestPractices.Samples
{
    /// <summary>Owns object-lifetime state and bindings to the UIDocument's current visual tree.</summary>
    [RequireComponent(typeof(UIDocument))]
    public sealed class SampleView : MonoBehaviour, ICounterView
    {
        private const string k_countName = "counter__count";
        private const string k_incrementName = "counter__increment-button";

        private readonly CounterModel m_model = new CounterModel();
        private UIDocument m_document;
        private VisualElement m_boundRoot;
        private VisualElement m_failedRoot;
        private Label m_countLabel;
        private Button m_incrementButton;
        private SamplePresenter m_presenter;

        public int Count => m_model.Count;
        public event Action IncrementRequested;

        private void Awake()
        {
            m_document = GetComponent<UIDocument>();
        }

        private void OnEnable()
        {
            m_failedRoot = null;
            BindCurrentTree();
        }

        private void OnDisable()
        {
            Unbind();
        }

        private void Update()
        {
            // UIDocument can replace its root independently of this component's enable lifetime.
            // A reference comparison catches either component-enable order without polling queries.
            if (m_document.rootVisualElement != m_boundRoot) BindCurrentTree();
        }

        public void SetCount(int count)
        {
            if (m_countLabel != null) m_countLabel.text = count.ToString();
        }

        private void BindCurrentTree()
        {
            VisualElement root = m_document.rootVisualElement;
            if (root == m_boundRoot || root == m_failedRoot) return;
            Unbind();
            if (root == null) return;

            Label countLabel = root.Q<Label>(k_countName);
            Button incrementButton = root.Q<Button>(k_incrementName);
            if (countLabel == null || incrementButton == null)
            {
                m_failedRoot = root;
                Debug.LogError("Counter UXML must contain its count label and increment button.", this);
                return;
            }

            m_boundRoot = root;
            m_countLabel = countLabel;
            m_incrementButton = incrementButton;
            try
            {
                m_presenter = new SamplePresenter(m_model, this);
                m_incrementButton.clicked += HandleIncrementClicked;
                m_boundRoot.RegisterCallback<DetachFromPanelEvent>(HandleTreeDetached);
            }
            catch
            {
                Unbind();
                throw;
            }
        }

        private void Unbind()
        {
            if (m_boundRoot != null)
                m_boundRoot.UnregisterCallback<DetachFromPanelEvent>(HandleTreeDetached);
            if (m_incrementButton != null) m_incrementButton.clicked -= HandleIncrementClicked;
            m_presenter?.Dispose();
            m_presenter = null;
            m_incrementButton = null;
            m_countLabel = null;
            m_boundRoot = null;
        }

        private void HandleTreeDetached(DetachFromPanelEvent evt)
        {
            if (evt.target == m_boundRoot) Unbind();
        }

        private void HandleIncrementClicked()
        {
            IncrementRequested?.Invoke();
        }
    }
}
