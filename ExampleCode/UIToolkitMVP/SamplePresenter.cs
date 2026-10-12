using System;

namespace UnityBestPractices.Samples
{
    /// <summary>Connects one bound view to existing state; disposal stops presentation reactions.</summary>
    public sealed class SamplePresenter : IDisposable
    {
        private readonly CounterModel m_model;
        private readonly ICounterView m_view;
        private bool m_isDisposed;

        public SamplePresenter(CounterModel model, ICounterView view)
        {
            m_model = model ?? throw new ArgumentNullException(nameof(model));
            m_view = view ?? throw new ArgumentNullException(nameof(view));
            // Render before subscribing so a failed render cannot leave a partial subscription.
            m_view.SetCount(m_model.Count);
            m_view.IncrementRequested += HandleIncrementRequested;
        }

        public void Dispose()
        {
            if (m_isDisposed) return;
            m_isDisposed = true;
            m_view.IncrementRequested -= HandleIncrementRequested;
        }

        private void HandleIncrementRequested()
        {
            if (m_isDisposed) return;
            m_model.Increment();
            m_view.SetCount(m_model.Count);
        }
    }
}
