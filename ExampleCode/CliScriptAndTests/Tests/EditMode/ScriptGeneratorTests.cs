using System;
using System.IO;
using NUnit.Framework;
using UnityEditor;

namespace UnityBestPractices.Samples.Cli.Tests
{
    public sealed class ScriptGeneratorTests
    {
        private string m_folder;

        [SetUp]
        public void SetUp()
        {
            string name = "ScriptGeneratorFixture" + Guid.NewGuid().ToString("N");
            string guid = AssetDatabase.CreateFolder("Assets", name);
            m_folder = AssetDatabase.GUIDToAssetPath(guid);
        }

        [TearDown]
        public void TearDown()
        {
            AssetDatabase.DeleteAsset(m_folder);
        }

        [Test]
        public void Preview_WritesNeitherScriptNorMetadata()
        {
            string path = m_folder + "/Preview.cs";
            Assert.That(ScriptGenerator.Generate(path, "// fixture source\n", true), Does.StartWith("WouldCreate:"));
            Assert.That(File.Exists(path), Is.False);
            Assert.That(File.Exists(path + ".meta"), Is.False);
        }

        [Test]
        public void Rerun_PreservesGuidAndConflictingSource()
        {
            string path = m_folder + "/Created.cs";
            const string source = "// fixture source\n";
            Assert.That(ScriptGenerator.Generate(path, source, false), Does.StartWith("Created:"));
            string guid = AssetDatabase.AssetPathToGUID(path);
            Assert.That(guid, Is.Not.Empty);
            string metadata = File.ReadAllText(path + ".meta");
            Assert.That(ScriptGenerator.Generate(path, source, false), Does.StartWith("Unchanged:"));
            Assert.That(AssetDatabase.AssetPathToGUID(path), Is.EqualTo(guid));
            Assert.That(File.ReadAllText(path + ".meta"), Is.EqualTo(metadata));
            Assert.Throws<InvalidOperationException>(() => ScriptGenerator.Generate(path, "// different\n", false));
            Assert.That(File.ReadAllText(path), Is.EqualTo(source));
            Assert.That(File.ReadAllText(path + ".meta"), Is.EqualTo(metadata));
        }

        [TestCase("../Outside.cs")]
        [TestCase("Assets/../Outside.cs")]
        [TestCase("Assets/Example.asset")]
        public void InvalidDestination_IsRejected(string path)
        {
            Assert.Throws<ArgumentException>(() => ScriptGenerator.Generate(path, "// fixture\n", false));
        }
    }
}
