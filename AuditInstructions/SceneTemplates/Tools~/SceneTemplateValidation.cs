using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.PackageManager;
using UnityEditor.SceneManagement;
using UnityEditor.SceneTemplate;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.UIElements;

namespace UnityStarter.SceneTemplates.Authoring
{
    /// <summary>Explicit validation/authoring operations for a disposable consumer project only.</summary>
    public static class SceneTemplateValidation
    {
        private const string k_root = "Assets/StrategyStarter/SceneTemplates";
        private static string EvidenceDirectory => Path.Combine(Directory.GetParent(Application.dataPath).FullName, "ValidationResults");

        /// <summary>Instantiates two scenes per template, verifies saved dependency ownership, and reports all dependencies.</summary>
        public static void Prepare()
        {
            Directory.CreateDirectory(EvidenceDirectory);
            AssetDatabase.Refresh();
            Require(!AssetDatabase.IsValidFolder("Assets/Generated"), "Use a fresh disposable consumer; Assets/Generated already exists.");
            AssetDatabase.CreateFolder("Assets", "Generated");

            var report = new System.Text.StringBuilder();
            foreach (string name in new[] { "StrategySandbox", "UIPreview", "AssetLookDev" })
            {
                string sourcePath = k_root + "/" + name + "/" + name + ".scenetemplate";
                var template = AssetDatabase.LoadAssetAtPath<SceneTemplateAsset>(sourcePath);
                Require(template != null && template.isValid && template.addToDefaults, "Invalid/unlisted template: " + name);
                Require(template.preview != null, "Missing imported preview: " + name);
                report.AppendLine(name);
                foreach (var dependency in template.dependencies)
                {
                    report.AppendLine(dependency.instantiationMode + " " + AssetDatabase.GetAssetPath(dependency.dependency));
                }

                for (int i = 0; i < 2; i++)
                {
                    string scenePath = "Assets/Generated/" + name + i + ".unity";
                    var result = SceneTemplateService.Instantiate(template, false, scenePath);
                    Require(result != null && result.scene.IsValid(), "Instantiation failed: " + scenePath);
                    EditorSceneManager.SaveScene(result.scene, scenePath);
                    var saved = EditorSceneManager.OpenScene(scenePath, OpenSceneMode.Single);
                    foreach (var root in saved.GetRootGameObjects())
                    {
                        foreach (var transform in root.GetComponentsInChildren<Transform>(true))
                        {
                            Require(GameObjectUtility.GetMonoBehavioursWithMissingScriptCount(transform.gameObject) == 0,
                                "Missing script: " + transform.name);
                        }
                    }

                    Require(UnityEngine.Object.FindObjectsByType<Camera>().Length == 1, "Camera count");
                    Require(UnityEngine.Object.FindObjectsByType<AudioListener>().Length == 1, "Listener count");
                    if (name == "UIPreview")
                    {
                        var document = UnityEngine.Object.FindAnyObjectByType<UIDocument>();
                        Require(document != null && document.visualTreeAsset != null && document.panelSettings != null, "UI refs");
                        Require(AssetDatabase.GetAssetPath(document.panelSettings).StartsWith("Assets/Generated/"), "Panel not cloned");
                        Require(AssetDatabase.GetAssetPath(document.visualTreeAsset).StartsWith("Assets/Generated/"), "UXML not cloned");
                        Require(AssetDatabase.GetAssetPath(document.panelSettings.themeStyleSheet).StartsWith("Assets/Generated/"), "Theme not cloned");
                    }
                    else
                    {
                        var volume = UnityEngine.Object.FindAnyObjectByType<Volume>();
                        Require(volume != null && volume.sharedProfile != null && volume.sharedProfile.components.Count == 1, "Volume refs");
                        Require(AssetDatabase.GetAssetPath(volume.sharedProfile).StartsWith("Assets/Generated/"), "Volume not cloned");
                    }

                    foreach (string dependency in AssetDatabase.GetDependencies(scenePath, true))
                    {
                        Require(!dependency.StartsWith("Assets/") || dependency.StartsWith(k_root + "/")
                            || dependency.StartsWith("Assets/Generated/"), "Unexpected asset dependency: " + dependency);
                    }
                    report.AppendLine("REOPENED " + scenePath);
                }
            }

            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            EditorBuildSettings.scenes = new[] { "StrategySandbox", "UIPreview", "AssetLookDev" }
                .Select(name => new EditorBuildSettingsScene("Assets/Generated/" + name + "0.unity", true)).ToArray();
            AssetDatabase.SaveAssets();
            File.WriteAllText(EvidenceDirectory + "/dependency-validation.txt", report.ToString());
            Debug.Log("SCENE_TEMPLATE_PREPARE_PASS: six generated scenes reopened; references and dependencies valid");
        }

        /// <summary>Installs the test package through Package Manager in this disposable project.</summary>
        public static void InstallTests()
        {
            Directory.CreateDirectory(EvidenceDirectory);
            var request = Client.Add("com.unity.test-framework");
            var deadline = DateTime.UtcNow.AddMinutes(3);
            while (!request.IsCompleted && DateTime.UtcNow < deadline)
            {
                System.Threading.Thread.Sleep(100);
            }

            Require(request.IsCompleted && request.Status == StatusCode.Success, "Test Framework install failed: " + request.Error?.message);
            File.WriteAllText(EvidenceDirectory + "/test-package.txt", request.Result.packageId);
        }

        /// <summary>Builds an ordinary macOS player with all three generated scenes.</summary>
        public static void Build()
        {
            Directory.CreateDirectory(EvidenceDirectory);
            var scenes = new[] { "StrategySandbox", "UIPreview", "AssetLookDev" }
                .Select(name => "Assets/Generated/" + name + "0.unity").ToArray();
            EditorBuildSettings.scenes = scenes.Select(path => new EditorBuildSettingsScene(path, true)).ToArray();
            PlayerSettings.defaultScreenWidth = 1280;
            PlayerSettings.defaultScreenHeight = 720;
            PlayerSettings.fullScreenMode = FullScreenMode.Windowed;
            PlayerSettings.runInBackground = true;
            var result = BuildPipeline.BuildPlayer(new BuildPlayerOptions
            {
                scenes = scenes,
                locationPathName = EvidenceDirectory + "/Player/SceneTemplates.app",
                target = BuildTarget.StandaloneOSX,
                options = BuildOptions.None
            });
            Require(result.summary.result == BuildResult.Succeeded, "Normal player build failed");
            File.WriteAllText(EvidenceDirectory + "/player-build.txt", result.summary.result + " / " + result.summary.totalSize + " bytes");
        }

        private static void Require(bool condition, string message)
        {
            if (!condition)
            {
                throw new InvalidOperationException(message);
            }
        }
    }
}
