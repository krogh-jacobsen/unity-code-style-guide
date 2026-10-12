using System;
using NUnit.Framework;

namespace UnityBestPractices.Samples.Tests
{
    public sealed class SamplePresenterTests
    {
        [Test]
        public void Bind_RendersExistingState_AndEachRequestIncrementsOnce()
        {
            var model = new CounterModel();
            model.Increment();
            var view = new FakeView();
            using (var presenter = new SamplePresenter(model, view))
            {
                Assert.That(view.DisplayedCount, Is.EqualTo(1));
                view.RequestIncrement();
                Assert.That(model.Count, Is.EqualTo(2));
                Assert.That(view.DisplayedCount, Is.EqualTo(2));
            }
        }

        [Test]
        public void Dispose_IsRepeatable_AndRebindingPreservesState()
        {
            var model = new CounterModel();
            var view = new FakeView();
            var presenter = new SamplePresenter(model, view);
            view.RequestIncrement();
            presenter.Dispose();
            presenter.Dispose();
            view.RequestIncrement();
            Assert.That(model.Count, Is.EqualTo(1));
            using (var rebound = new SamplePresenter(model, view))
            {
                Assert.That(view.DisplayedCount, Is.EqualTo(1));
                view.RequestIncrement();
                Assert.That(model.Count, Is.EqualTo(2));
            }
        }

        [Test]
        public void FailedInitialRender_LeavesNoSubscription()
        {
            var model = new CounterModel();
            var view = new FakeView { ShouldFailRender = true };
            Assert.Throws<InvalidOperationException>(() => new SamplePresenter(model, view));
            view.RequestIncrement();
            Assert.That(model.Count, Is.Zero);
        }

        private sealed class FakeView : ICounterView
        {
            public int DisplayedCount { get; private set; }
            public bool ShouldFailRender { get; set; }
            public event Action IncrementRequested;

            public void RequestIncrement() => IncrementRequested?.Invoke();

            public void SetCount(int count)
            {
                if (ShouldFailRender) throw new InvalidOperationException("Fixture render failure.");
                DisplayedCount = count;
            }
        }
    }
}
