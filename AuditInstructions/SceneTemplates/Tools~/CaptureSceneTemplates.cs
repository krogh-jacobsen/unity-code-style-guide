using System;
using System.Collections;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UIElements;
using UnityStarter.SceneTemplates;

namespace UnityStarter.SceneTemplates.Authoring
{
    /// <summary>Temporary graphical acceptance probe; excluded from shipped starter resources.</summary>
    public sealed class CaptureSceneTemplates : MonoBehaviour
    {
        private string m_output;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        private static void Boot()
        {
            if (Array.IndexOf(Environment.GetCommandLineArgs(), "-scene-template-capture") < 0)
            {
                return;
            }

            var host = new GameObject("Temporary acceptance capture", typeof(CaptureSceneTemplates));
            DontDestroyOnLoad(host);
        }

        private IEnumerator Start()
        {
            m_output = Path.Combine(Application.persistentDataPath, "SceneTemplateCaptures");
            string[] args = Environment.GetCommandLineArgs();
            int outputIndex = Array.IndexOf(args, "-sceneTemplateCaptures");
            if (outputIndex >= 0 && outputIndex + 1 < args.Length)
            {
                m_output = args[outputIndex + 1];
            }

            Directory.CreateDirectory(m_output);
            foreach (string name in new[] { "StrategySandbox", "AssetLookDev", "UIPreview" })
            {
                yield return SceneManager.LoadSceneAsync("Assets/Generated/" + name + "0.unity");
                for (int i = 0; i < 12; i++)
                {
                    yield return null;
                }

                yield return new WaitForSecondsRealtime(0.5f);
                yield return new WaitForEndOfFrame();
                Save(name);
                if (name == "UIPreview")
                {
                    var root = FindAnyObjectByType<UIDocument>().rootVisualElement;
                    var open = root.Q<Button>("openModal");
                    using (var evt = NavigationSubmitEvent.GetPooled())
                    {
                        evt.target = open;
                        open.SendEvent(evt);
                    }

                    yield return new WaitForEndOfFrame();
                    Save("UIPreviewModal");
                    Screen.SetResolution(800, 600, FullScreenMode.Windowed);
                    for (int i = 0; i < 12; i++)
                    {
                        yield return null;
                    }

                    yield return new WaitForEndOfFrame();
                    Save("UIPreview800x600");
                }
            }

            File.WriteAllText(m_output + "/complete.txt", "Three templates rendered; modal and 800x600 captured");
            Application.Quit();
        }

        private void Save(string name)
        {
            var texture = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(m_output + "/" + name + ".png", texture.EncodeToPNG());
            Destroy(texture);
        }
    }
}
