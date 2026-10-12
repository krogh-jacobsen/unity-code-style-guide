namespace UnityBestPractices.Samples
{
    /// <summary>Counter state lives for the host object's lifetime.</summary>
    public sealed class CounterModel
    {
        public int Count { get; private set; }

        public void Increment()
        {
            Count++;
        }
    }
}
