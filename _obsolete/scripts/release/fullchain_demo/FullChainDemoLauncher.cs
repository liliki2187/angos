using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

internal static class FullChainDemoLauncher
{
    [STAThread]
    private static int Main()
    {
        var root = AppDomain.CurrentDomain.BaseDirectory;
        var entryCandidates = new[]
        {
            Path.Combine(root, "index.html"),
            Path.Combine(root, "web", "world-mysteries-full-chain.html"),
        };

        string entryPath = null;
        foreach (var candidate in entryCandidates)
        {
            if (File.Exists(candidate))
            {
                entryPath = candidate;
                break;
            }
        }

        if (entryPath == null)
        {
            MessageBox.Show(
                "Entry file not found. Make sure index.html and the web folder are next to this EXE.",
                "Run FullChain Demo",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            return 1;
        }

        try
        {
            Process.Start(new ProcessStartInfo
            {
                FileName = entryPath,
                UseShellExecute = true,
                WorkingDirectory = Path.GetDirectoryName(entryPath) ?? root,
            });
            return 0;
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                "Failed to open the prototype:\n" + ex.Message,
                "Run FullChain Demo",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            return 1;
        }
    }
}
