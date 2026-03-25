using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

public class BuildScript
{
    public static void BuildGame()
    {
        // Get build options
        string[] scenes = new string[] { "Assets/Scenes/MainMenu.unity" };
        string buildPath = System.Environment.GetEnvironmentVariable("BUILD_PATH") ?? "build";
        string targetPlatform = System.Environment.GetEnvironmentVariable("TARGET_PLATFORM") ?? "StandaloneWindows64";
        string buildName = System.Environment.GetEnvironmentVariable("BUILD_NAME") ?? "Angus";
        
        BuildTarget target = BuildTarget.StandaloneWindows64;
        switch (targetPlatform)
        {
            case "StandaloneOSX":
                target = BuildTarget.StandaloneOSX;
                break;
            case "StandaloneLinux64":
                target = BuildTarget.StandaloneLinux64;
                break;
            default:
                target = BuildTarget.StandaloneWindows64;
                break;
        }
        
        // Build options
        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = scenes,
            locationPathName = $"{buildPath}/{targetPlatform}/{buildName}.exe",
            target = target,
            options = BuildOptions.None
        };
        
        // Execute build
        BuildSummary summary = BuildPipeline.BuildPlayer(options).summary;
        
        if (summary.result == BuildResult.Succeeded)
        {
            Debug.Log($"Build succeeded: {summary.totalSize} bytes");
        }
        else
        {
            Debug.Log($"Build failed: {summary.result}");
            EditorApplication.Exit((int)summary.result);
        }
    }
}