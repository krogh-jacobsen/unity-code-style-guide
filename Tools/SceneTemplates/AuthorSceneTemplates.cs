using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditor.SceneTemplate;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.UIElements;
using UnityStarter.SceneTemplates;

namespace UnityStarter.SceneTemplates.Authoring
{
    /// <summary>Disposable-project authoring entry point. Creates new assets; refuses to overwrite templates.</summary>
    public sealed class AuthorSceneTemplates
    {
        private const string k_root = "Assets/StarterSceneTemplates";
        private Material m_ground;
        private Material m_stone;
        private Material m_accent;
        private GameObject m_rig;

        /// <summary>Creates all three templates and their explicitly scoped dependencies.</summary>
        public static void Create()
        {
            new AuthorSceneTemplates().CreateResources();
        }

        /// <summary>Assigns actual player captures from the project's Captures folder to the template previews.</summary>
        public static void AttachPreviews()
        {
            string project = Directory.GetParent(Application.dataPath).FullName;
            foreach (string name in new[] { "StrategySandbox", "UIPreview", "AssetLookDev" })
            {
                string path = k_root + "/" + name + "/Preview.png";
                File.Copy(Path.Combine(project, "Captures", name + ".png"), path, true);
                AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceSynchronousImport);
                var importer = (TextureImporter)AssetImporter.GetAtPath(path);
                importer.textureType = TextureImporterType.Default;
                importer.maxTextureSize = 1024;
                importer.mipmapEnabled = false;
                importer.textureCompression = TextureImporterCompression.Uncompressed;
                importer.SaveAndReimport();
                var template = AssetDatabase.LoadAssetAtPath<SceneTemplateAsset>(k_root + "/" + name + "/" + name + ".scenetemplate");
                template.preview = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
                EditorUtility.SetDirty(template);
            }

            if (AssetDatabase.IsValidFolder(k_root + "/Shared/Lighting"))
            {
                AssetDatabase.DeleteAsset(k_root + "/Shared/Lighting");
            }

            AssetDatabase.SaveAssets();
        }

        private void CreateResources()
        {
            if (AssetDatabase.LoadAssetAtPath<SceneTemplateAsset>(k_root + "/StrategySandbox/StrategySandbox.scenetemplate") != null)
            {
                throw new InvalidOperationException("Templates already exist. Use a fresh authoring project.");
            }

            Folder(k_root + "/Shared/Materials");
            Folder(k_root + "/StrategySandbox");
            Folder(k_root + "/AssetLookDev");
            AssetDatabase.Refresh();
            m_ground = Material("Ground", new Color(0.24f, 0.29f, 0.29f), 0.05f);
            m_stone = Material("Stone", new Color(0.61f, 0.66f, 0.66f), 0.2f);
            m_accent = Material("Accent", new Color(0.75f, 0.48f, 0.18f), 0.35f);
            CreateInputAndRig();
            CreateWorld("StrategySandbox", false);
            CreateWorld("AssetLookDev", true);
            CreateUI();
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            AssetDatabase.SaveAssets();
            File.WriteAllText(Path.Combine(Directory.GetParent(Application.dataPath).FullName, "authored.txt"), "Three templates authored");
        }

        private void CreateInputAndRig()
        {
            var definition = ScriptableObject.CreateInstance<InputActionAsset>();
            var map = definition.AddActionMap("Camera");
            var pan = map.AddAction("Pan", InputActionType.Value, expectedControlLayout: "Vector2");
            pan.AddCompositeBinding("2DVector").With("Up", "<Keyboard>/w").With("Down", "<Keyboard>/s")
                .With("Left", "<Keyboard>/a").With("Right", "<Keyboard>/d");
            pan.AddCompositeBinding("2DVector").With("Up", "<Keyboard>/upArrow").With("Down", "<Keyboard>/downArrow")
                .With("Left", "<Keyboard>/leftArrow").With("Right", "<Keyboard>/rightArrow");
            var rotate = map.AddAction("Rotate", InputActionType.Value, expectedControlLayout: "Axis");
            rotate.AddCompositeBinding("1DAxis").With("Negative", "<Keyboard>/q").With("Positive", "<Keyboard>/e");
            map.AddAction("Zoom", InputActionType.PassThrough, "<Mouse>/scroll/y", expectedControlLayout: "Axis");
            map.AddAction("Drag", InputActionType.Button, "<Mouse>/middleButton");
            map.AddAction("Look", InputActionType.PassThrough, "<Mouse>/delta", expectedControlLayout: "Vector2");
            var sprint = map.AddAction("Sprint", InputActionType.Button, "<Keyboard>/leftShift");
            sprint.AddBinding("<Keyboard>/rightShift");
            map.AddAction("ToggleProjection", InputActionType.Button, "<Keyboard>/tab");
            definition.name = "StrategyCameraActions";
            string actionPath = k_root + "/Shared/Camera/StrategyCameraActions.inputactions";
            File.WriteAllText(actionPath, definition.ToJson());
            UnityEngine.Object.DestroyImmediate(definition);
            AssetDatabase.ImportAsset(actionPath, ImportAssetOptions.ForceSynchronousImport);
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var rig = new GameObject("StrategyCameraRig");
            rig.SetActive(false);
            var pivot = new GameObject("PitchPivot").transform;
            pivot.SetParent(rig.transform, false);
            pivot.localRotation = Quaternion.Euler(43f, 0f, 0f);
            var lensObject = new GameObject("Main Camera", typeof(Camera), typeof(AudioListener));
            lensObject.tag = "MainCamera";
            lensObject.transform.SetParent(pivot, false);
            lensObject.transform.localPosition = new Vector3(0f, 0f, -55f);
            var camera = lensObject.GetComponent<Camera>();
            camera.fieldOfView = 50f;
            camera.nearClipPlane = 0.3f;
            camera.farClipPlane = 600f;
            camera.backgroundColor = new Color(0.12f, 0.17f, 0.21f);
            camera.clearFlags = CameraClearFlags.SolidColor;
            camera.GetUniversalAdditionalCameraData().renderPostProcessing = true;
            var controller = rig.AddComponent<StrategyCameraController>();
            var serialized = new SerializedObject(controller);
            serialized.FindProperty("m_pitchPivot").objectReferenceValue = pivot;
            serialized.FindProperty("m_lens").objectReferenceValue = camera;
            serialized.FindProperty("m_inputDefinition").objectReferenceValue = AssetDatabase.LoadAssetAtPath<InputActionAsset>(actionPath);
            serialized.ApplyModifiedPropertiesWithoutUndo();
            rig.SetActive(true);
            m_rig = PrefabUtility.SaveAsPrefabAsset(rig, k_root + "/Shared/Camera/StrategyCameraRig.prefab");
            UnityEngine.Object.DestroyImmediate(rig);
        }

        private void CreateWorld(string name, bool isLookDev)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var rig = (GameObject)PrefabUtility.InstantiatePrefab(m_rig);
            rig.transform.position = new Vector3(0f, 0f, 3f);
            rig.transform.rotation = Quaternion.Euler(0f, 25f, 0f);
            var world = new GameObject("World").transform;
            var ground = Primitive("Ground / 1 unit = 1 metre", PrimitiveType.Plane, world,
                Vector3.zero, new Vector3(16f, 1f, 16f), m_ground);
            var content = new GameObject(isLookDev ? "DisplaySlots" : "Experiments").transform;
            content.SetParent(world, false);
            if (isLookDev)
            {
                string[] labels = { "Buildings", "Props", "Vegetation" };
                for (int i = 0; i < labels.Length; i++)
                {
                    var slot = new GameObject(labels[i]).transform;
                    slot.SetParent(content, false);
                    slot.localPosition = new Vector3((i - 1) * 14f, 0f, 0f);
                    Primitive("Display plinth", PrimitiveType.Cube, slot, new Vector3(0f, 0.25f, 0f),
                        new Vector3(11f, 0.5f, 11f), m_stone);
                    Primitive("Replace with your asset", PrimitiveType.Cube, slot, new Vector3(0f, 2.5f, 0f),
                        new Vector3(4f, 4f, 4f), i == 1 ? m_accent : m_stone);
                    Label(labels[i], slot, new Vector3(-4f, 0.55f, -4f));
                }

                var samples = new GameObject("MaterialSamples").transform;
                samples.SetParent(world, false);
                for (int i = 0; i < 3; i++)
                {
                    Primitive("Material sample", PrimitiveType.Sphere, samples, new Vector3((i - 1) * 4f, 1f, -11f),
                        Vector3.one * 2f, i == 0 ? m_ground : i == 1 ? m_stone : m_accent);
                }
            }
            else
            {
                Primitive("Building scale / 6 x 4 x 6 m", PrimitiveType.Cube, content, new Vector3(0f, 2f, 0f),
                    new Vector3(6f, 4f, 6f), m_accent);
                Primitive("Tower scale / 2 x 8 x 2 m", PrimitiveType.Cube, content, new Vector3(10f, 4f, 5f),
                    new Vector3(2f, 8f, 2f), m_stone);
            }

            Primitive("Human scale / 2 m", PrimitiveType.Capsule, world, new Vector3(-7f, 1f, -5f), Vector3.one, m_stone);
            Environment(name);
            Label("WASD / arrows: pan   Q/E: rotate   Wheel: zoom\nShift: faster   MMB drag: orbit   Tab: projection", world,
                new Vector3(-12f, 0.05f, -14f));
            string scenePath = k_root + "/" + name + "/" + name + ".unity";
            EditorSceneManager.SaveScene(scene, scenePath);
            MakeTemplate(name, scenePath, isLookDev ? "Compare asset scale, materials and silhouettes under neutral strategy-game lighting."
                : "Standalone strategy camera, neutral lighting and metre-scale primitives. No game session required.");
        }

        private void Environment(string sceneName)
        {
            var environment = new GameObject("Environment").transform;
            var sun = new GameObject("Sun", typeof(Light)).GetComponent<Light>();
            sun.transform.SetParent(environment, false);
            sun.type = LightType.Directional;
            sun.transform.rotation = Quaternion.Euler(48f, -35f, 0f);
            sun.intensity = 2f;
            sun.color = new Color(1f, 0.96f, 0.88f);
            sun.shadows = LightShadows.Soft;
            RenderSettings.sun = sun;
            var fill = new GameObject("Fill", typeof(Light)).GetComponent<Light>();
            fill.transform.SetParent(environment, false);
            fill.type = LightType.Directional;
            fill.transform.rotation = Quaternion.Euler(50f, 145f, 0f);
            fill.intensity = 0.5f;
            fill.shadows = LightShadows.None;
            RenderSettings.ambientMode = AmbientMode.Flat;
            RenderSettings.ambientLight = new Color(0.55f, 0.59f, 0.62f);
            RenderSettings.ambientSkyColor = new Color(0.54f, 0.62f, 0.7f);
            RenderSettings.ambientEquatorColor = new Color(0.35f, 0.4f, 0.43f);
            RenderSettings.ambientGroundColor = new Color(0.18f, 0.2f, 0.23f);
            RenderSettings.fog = false;
            RenderSettings.skybox = null;
            var profile = ScriptableObject.CreateInstance<VolumeProfile>();
            AssetDatabase.CreateAsset(profile, k_root + "/" + sceneName + "/NeutralVolume.asset");
            var tonemapping = profile.Add<Tonemapping>();
            AssetDatabase.AddObjectToAsset(tonemapping, profile);
            tonemapping.mode.Override(TonemappingMode.None);
            var volume = new GameObject("Global Volume", typeof(Volume)).GetComponent<Volume>();
            volume.transform.SetParent(environment, false);
            volume.isGlobal = true;
            volume.sharedProfile = profile;
            EditorUtility.SetDirty(profile);
        }

        private void CreateUI()
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var camera = new GameObject("Main Camera", typeof(Camera), typeof(AudioListener)).GetComponent<Camera>();
            camera.tag = "MainCamera";
            camera.clearFlags = CameraClearFlags.SolidColor;
            camera.backgroundColor = new Color(0.06f, 0.09f, 0.11f);
            camera.cullingMask = 0;
            var panel = ScriptableObject.CreateInstance<PanelSettings>();
            panel.scaleMode = PanelScaleMode.ScaleWithScreenSize;
            panel.referenceResolution = new Vector2Int(1280, 720);
            panel.screenMatchMode = PanelScreenMatchMode.MatchWidthOrHeight;
            panel.match = 0.5f;
            panel.themeStyleSheet = AssetDatabase.LoadAssetAtPath<ThemeStyleSheet>(k_root + "/UIPreview/PreviewTheme.tss");
            AssetDatabase.CreateAsset(panel, k_root + "/UIPreview/PreviewPanelSettings.asset");
            var host = new GameObject("UI Preview");
            host.SetActive(false);
            var document = host.AddComponent<UIDocument>();
            document.panelSettings = panel;
            document.visualTreeAsset = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>(k_root + "/UIPreview/PreviewScreen.uxml");
            host.AddComponent<PreviewScreen>();
            host.SetActive(true);
            string path = k_root + "/UIPreview/UIPreview.unity";
            EditorSceneManager.SaveScene(scene, path);
            MakeTemplate("UIPreview", path, "Strategy HUD, catalogue, controls and modal focus. Sample data only; no game framework.");
        }

        private void MakeTemplate(string name, string scenePath, string description)
        {
            var template = SceneTemplateService.CreateTemplateFromScene(AssetDatabase.LoadAssetAtPath<SceneAsset>(scenePath),
                k_root + "/" + name + "/" + name + ".scenetemplate");
            template.templateName = name == "UIPreview" ? "Strategy / UI Preview" : name == "AssetLookDev"
                ? "Strategy / Asset LookDev" : "Strategy / Sandbox";
            template.description = description;
            template.addToDefaults = true;
            foreach (var dependency in template.dependencies)
            {
                string path = AssetDatabase.GetAssetPath(dependency.dependency);
                bool isEditable = dependency.dependency is VolumeProfile || dependency.dependency is PanelSettings
                    || dependency.dependency is VisualTreeAsset || dependency.dependency is StyleSheet;
                dependency.instantiationMode = path.StartsWith(k_root + "/" + name + "/", StringComparison.Ordinal) && isEditable
                    ? TemplateInstantiationMode.Clone : TemplateInstantiationMode.Reference;
            }

            EditorUtility.SetDirty(template);
            AssetDatabase.SaveAssets();
        }

        private Material Material(string name, Color color, float smoothness)
        {
            var material = new Material(Shader.Find("Universal Render Pipeline/Lit"));
            material.name = name;
            material.SetColor("_BaseColor", color);
            material.SetFloat("_Smoothness", smoothness);
            AssetDatabase.CreateAsset(material, k_root + "/Shared/Materials/" + name + ".mat");
            return material;
        }

        private GameObject Primitive(string name, PrimitiveType type, Transform parent, Vector3 position,
            Vector3 scale, Material material)
        {
            var result = GameObject.CreatePrimitive(type);
            result.name = name;
            result.transform.SetParent(parent, false);
            result.transform.localPosition = position;
            result.transform.localScale = scale;
            result.GetComponent<Renderer>().sharedMaterial = material;
            return result;
        }

        private void Label(string text, Transform parent, Vector3 position)
        {
            var label = new GameObject("Label / " + text.Split('\n')[0], typeof(TextMesh)).GetComponent<TextMesh>();
            label.transform.SetParent(parent, false);
            label.transform.localPosition = position;
            label.transform.localRotation = Quaternion.Euler(90f, 0f, 0f);
            label.text = text;
            label.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            label.GetComponent<MeshRenderer>().sharedMaterial = label.font.material;
            label.fontSize = 48;
            label.characterSize = 0.12f;
            label.color = new Color(0.025f, 0.035f, 0.04f);
        }

        private void Folder(string path)
        {
            if (AssetDatabase.IsValidFolder(path))
            {
                return;
            }

            string parent = path.Substring(0, path.LastIndexOf('/'));
            Folder(parent);
            AssetDatabase.CreateFolder(parent, Path.GetFileName(path));
        }
    }
}
