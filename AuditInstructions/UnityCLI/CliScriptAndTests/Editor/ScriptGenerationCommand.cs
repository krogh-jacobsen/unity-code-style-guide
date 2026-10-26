using System;
using Unity.Pipeline.Commands;
using UnityEditor;
using UnityEngine;

namespace UnityBestPractices.Samples.Cli
{
    /// <summary>Small discoverable CLI command; the registered name belongs to this example only.</summary>
    public static class ScriptGenerationCommand
    {
        private const string k_exampleRoot = "Assets/Examples/CliScriptAndTests";

        /// <summary>Generates the sample score counter after previewing its owned destination.</summary>
        [CliCommand("starter_generate_score_counter", "Preview or create the sample score counter script.",
            MainThreadRequired = true)]
        public static string GenerateScoreCounter(
            [CliArg("dry_run", "Preview without writing source or metadata; defaults to true.")] bool dryRun = true)
        {
            string templatePath = k_exampleRoot + "/Templates/SampleScoreCounter.cs.txt";
            TextAsset template = AssetDatabase.LoadAssetAtPath<TextAsset>(templatePath);
            if (template == null)
            {
                throw new InvalidOperationException($"Install the complete example at {k_exampleRoot}.");
            }
            return ScriptGenerator.Generate(k_exampleRoot + "/Generated/SampleScoreCounter.cs", template.text, dryRun);
        }
    }
}
