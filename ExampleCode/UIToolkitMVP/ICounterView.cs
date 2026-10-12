using System;

namespace UnityBestPractices.Samples
{
    /// <summary>The presentation contract has no Unity dependency.</summary>
    public interface ICounterView
    {
        event Action IncrementRequested;
        void SetCount(int count);
    }
}
