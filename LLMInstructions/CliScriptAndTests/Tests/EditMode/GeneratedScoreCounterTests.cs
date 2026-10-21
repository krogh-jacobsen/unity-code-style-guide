using System;
using System.Reflection;
using NUnit.Framework;

namespace UnityBestPractices.Samples.Cli.Tests
{
    public sealed class GeneratedScoreCounterTests
    {
        private Type m_type;
        private object m_counter;

        [SetUp]
        public void SetUp()
        {
            // Reflection keeps the test assembly compilable before the first generation command.
            m_type = Type.GetType("UnityBestPractices.Samples.Cli.Generated.SampleScoreCounter, Starter.Cli.Generated");
            Assert.That(m_type, Is.Not.Null, "Run starter_generate_score_counter with dry_run=false and wait for compilation.");
            m_counter = Activator.CreateInstance(m_type);
        }

        [Test]
        public void AddScore_AccumulatesFromZero()
        {
            PropertyInfo score = m_type.GetProperty("Score");
            MethodInfo add = m_type.GetMethod("AddScore");
            Assert.That(score.GetValue(m_counter), Is.EqualTo(0));
            add.Invoke(m_counter, new object[] { 2 });
            add.Invoke(m_counter, new object[] { 3 });
            Assert.That(score.GetValue(m_counter), Is.EqualTo(5));
        }

        [Test]
        public void NegativeAmount_IsRejectedWithoutChangingScore()
        {
            MethodInfo add = m_type.GetMethod("AddScore");
            add.Invoke(m_counter, new object[] { 4 });
            TargetInvocationException exception = Assert.Throws<TargetInvocationException>(
                () => add.Invoke(m_counter, new object[] { -1 }));
            Assert.That(exception.InnerException, Is.TypeOf<ArgumentOutOfRangeException>());
            Assert.That(m_type.GetProperty("Score").GetValue(m_counter), Is.EqualTo(4));
        }
    }
}
