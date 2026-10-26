using System.Linq;
using NUnit.Framework;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditor.SceneTemplate;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Rendering;
using UnityEngine.UIElements;

namespace UnityStarter.SceneTemplates.Tests
{
    /// <summary>Checks the scenes created by the disposable consumer preparation workflow.</summary>
    public sealed class SceneTemplateTests
    {
        private const string k_root = "Assets/StrategyStarter/SceneTemplates";

        [TearDown]
        public void TearDown()
        {
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        }

        [TestCase("StrategySandbox")]
        [TestCase("UIPreview")]
        [TestCase("AssetLookDev")]
        public void GeneratedScenesHaveIndependentEditableAssets(string name)
        {
            var template = AssetDatabase.LoadAssetAtPath<SceneTemplateAsset>(k_root + "/" + name + "/" + name + ".scenetemplate");
            Assert.That(template.isValid && template.addToDefaults, Is.True);
            Object first;
            Object second;
            EditorSceneManager.OpenScene("Assets/Generated/" + name + "0.unity");
            first = name == "UIPreview" ? Object.FindAnyObjectByType<UIDocument>().panelSettings
                : Object.FindAnyObjectByType<Volume>().sharedProfile;
            EditorSceneManager.OpenScene("Assets/Generated/" + name + "1.unity");
            second = name == "UIPreview" ? Object.FindAnyObjectByType<UIDocument>().panelSettings
                : Object.FindAnyObjectByType<Volume>().sharedProfile;
            Assert.That(second, Is.Not.SameAs(first));
            Assert.That(AssetDatabase.GetAssetPath(first), Does.StartWith("Assets/Generated/"));
            Assert.That(AssetDatabase.GetAssetPath(second), Does.StartWith("Assets/Generated/"));
        }

        [Test]
        public void GeneratedUIReferencesItsOwnClonedThemeAndMarkup()
        {
            EditorSceneManager.OpenScene("Assets/Generated/UIPreview0.unity");
            var document = Object.FindAnyObjectByType<UIDocument>();
            string firstTree = AssetDatabase.GetAssetPath(document.visualTreeAsset);
            string firstTheme = AssetDatabase.GetAssetPath(document.panelSettings.themeStyleSheet);
            EditorSceneManager.OpenScene("Assets/Generated/UIPreview1.unity");
            document = Object.FindAnyObjectByType<UIDocument>();
            Assert.That(AssetDatabase.GetAssetPath(document.visualTreeAsset), Is.Not.EqualTo(firstTree));
            Assert.That(AssetDatabase.GetAssetPath(document.panelSettings.themeStyleSheet), Is.Not.EqualTo(firstTheme));
            Assert.That(AssetDatabase.GetDependencies(firstTheme), Has.Some.EndsWith(".uss"));
            Assert.That(AssetDatabase.GetDependencies(firstTheme).Where(path => path.EndsWith(".uss") && path.StartsWith("Assets/")),
                Has.All.StartsWith("Assets/Generated/UIPreview0/"));
        }

        [TestCase("StrategySandbox")]
        [TestCase("AssetLookDev")]
        public void WorldScenesRetainSharedPrefabInputAndValidMaterials(string name)
        {
            EditorSceneManager.OpenScene("Assets/Generated/" + name + "0.unity");
            var camera = Object.FindAnyObjectByType<StrategyCameraController>();
            Assert.That(PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(camera),
                Is.EqualTo(k_root + "/Shared/Camera/StrategyCameraRig.prefab"));
            var source = AssetDatabase.LoadAssetAtPath<InputActionAsset>(k_root + "/Shared/Camera/StrategyCameraActions.inputactions");
            Assert.That(source.FindActionMap("Camera", true).enabled, Is.False);
            foreach (var renderer in Object.FindObjectsByType<Renderer>())
            {
                Assert.That(renderer.sharedMaterial, Is.Not.Null, renderer.name);
                Assert.That(renderer.sharedMaterial.shader.name, Does.Not.Contain("InternalError"));
            }

            Assert.That(Object.FindAnyObjectByType<Volume>().sharedProfile.components.All(item => item != null), Is.True);
        }
    }
}
