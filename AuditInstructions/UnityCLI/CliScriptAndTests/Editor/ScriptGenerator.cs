using System;
using System.IO;
using System.Text;
using UnityEditor;
using UnityEngine;

namespace UnityBestPractices.Samples.Cli
{
    /// <summary>Creates owned C# source and lets Unity assign metadata; existing content is preserved.</summary>
    public static class ScriptGenerator
    {
        /// <summary>Previews or creates a .cs file in an existing Assets folder. Conflicts fail without overwrite.</summary>
        public static string Generate(string assetPath, string source, bool dryRun)
        {
            if (string.IsNullOrWhiteSpace(source))
            {
                throw new ArgumentException("Supply nonempty C# source.", nameof(source));
            }
            string fullPath = ValidatePath(assetPath);
            if (File.Exists(fullPath))
            {
                if (File.ReadAllText(fullPath) != source)
                {
                    throw new InvalidOperationException($"Existing script differs; review it manually: {assetPath}");
                }
                return $"Unchanged: {assetPath}";
            }
            if (File.Exists(fullPath + ".meta"))
            {
                throw new InvalidOperationException($"Orphan metadata requires investigation: {assetPath}");
            }
            if (dryRun)
            {
                return $"WouldCreate: {assetPath}";
            }

            // Source text is safe to author; Unity owns the imported asset's GUID and importer data.
            using (FileStream stream = new FileStream(fullPath, FileMode.CreateNew, FileAccess.Write))
            using (StreamWriter writer = new StreamWriter(stream, new UTF8Encoding(false)))
            {
                writer.Write(source);
            }
            AssetDatabase.ImportAsset(assetPath, ImportAssetOptions.ForceSynchronousImport);
            return $"Created: {assetPath}";
        }

        private static string ValidatePath(string assetPath)
        {
            if (string.IsNullOrEmpty(assetPath) || !assetPath.StartsWith("Assets/", StringComparison.Ordinal)
                || !assetPath.EndsWith(".cs", StringComparison.Ordinal) || assetPath.Contains("\\"))
            {
                throw new ArgumentException("Use an Assets-relative .cs path with forward slashes.");
            }
            string[] segments = assetPath.Split('/');
            foreach (string segment in segments)
            {
                if (segment == "." || segment == ".." || segment.Length == 0)
                {
                    throw new ArgumentException("Use a normalized Assets path without traversal.");
                }
            }
            string projectRoot = Directory.GetParent(Application.dataPath).FullName;
            string fullPath = Path.GetFullPath(Path.Combine(projectRoot, assetPath));
            string parentPath = Path.GetDirectoryName(fullPath);
            if (!Directory.Exists(parentPath))
            {
                throw new ArgumentException("Create the destination folder through AssetDatabase first.");
            }
            // A lexical Assets path must not escape through a linked folder or linked existing file.
            string current = fullPath;
            while (current != projectRoot)
            {
                if ((File.Exists(current) || Directory.Exists(current))
                    && (File.GetAttributes(current) & FileAttributes.ReparsePoint) != 0)
                {
                    throw new ArgumentException("Choose an owned destination without symbolic links.");
                }
                current = Path.GetDirectoryName(current);
            }
            return fullPath;
        }
    }
}
