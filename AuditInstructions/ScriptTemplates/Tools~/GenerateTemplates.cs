using System;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEngine;

public static class GenerateTemplates
{
    public static void Report()
    {
        Debug.Log("REPORT mode=" + EditorSettings.enterPlayModeOptions + " ns=" + EditorSettings.projectGenerationRootNamespace);
    }

    public static void Run()
    {
        string source = Environment.GetEnvironmentVariable("TEMPLATE_DIR");
        EditorSettings.enterPlayModeOptionsEnabled = true;
        EditorSettings.enterPlayModeOptions = EnterPlayModeOptions.DisableDomainReload;
        MethodInfo create = typeof(ProjectWindowUtil).GetMethod("CreateScriptAssetFromTemplate", BindingFlags.NonPublic | BindingFlags.Static);
        Debug.Log("GEN create method found: " + (create != null));
        foreach (string ns in new[] { "", "Sample.Game" })
        {
            EditorSettings.projectGenerationRootNamespace = ns;
            string label = ns == "" ? "Global" : "Namespaced";
            foreach (string file in Directory.GetFiles(source, "*.cs.txt", SearchOption.AllDirectories))
            {
                if (file.Contains("ReferenceOnly") || file.Contains("NetworkBehaviour") || file.Contains("Unit Test") || (Environment.GetEnvironmentVariable("ONLY") != null && !file.Contains(Environment.GetEnvironmentVariable("ONLY"))))
                {
                    continue;
                }
                string name = Path.GetFileName(file);
                name = name.Substring(name.LastIndexOf('-') + 1).Replace(".cs.txt", "");
                bool editorOnly = File.ReadAllText(file).Contains("UnityEditor");
                string dir = "Assets/Generated/" + label + (editorOnly ? "/Editor" : "");
                Directory.CreateDirectory(dir);
                create.Invoke(null, new object[] { dir + "/" + name + ".cs", file });
            }
        }
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
        Debug.Log("GEN done: " + Directory.GetFiles("Assets/Generated", "*.cs", SearchOption.AllDirectories).Length + " scripts");
    }
}
