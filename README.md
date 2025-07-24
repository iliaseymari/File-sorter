<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>

  <h1>📂 File Organizer – Smart File Sorting with Python</h1>

  <p>
    This project is a powerful and intelligent tool for <strong>automatically organizing files</strong> on your system. Built using Python and libraries like <code>tkinter</code>, <code>shutil</code>, and <code>tqdm</code>, it analyzes files in a selected folder and categorizes them into folders like Pictures, Music, Videos, Documents, and more.
  </p>

  <hr>

  <h2>📦 Required Libraries</h2>
  <ul>
    <li><code>tkinter</code> – for GUI folder selection ✅ (included by default in Python)</li>
    <li><code>argparse</code>, <code>json</code>, <code>os</code>, <code>threading</code>, <code>logging</code>, <code>shutil</code>, <code>pathlib</code> – ✅ all built-in modules</li>
    <li><code>tqdm</code> – ✅ <strong>used for progress bar</strong></li>
  </ul>

  <p>📥 To install <code>tqdm</code>, run:</p>
  <pre><code>pip install tqdm</code></pre>

  <hr>

  <h2>🚀 How to Run</h2>
  <ol>
    <li>Copy the code from <code>File-sorter.py</code>.</li>
    <li>Paste it into a Python file in your code editor.</li>
    <li>Install the libraries with the command we told you above..</li>
    <li>Run.</li>
  </ol>

  <p>📂 A folder selection dialog will appear asking you to choose the source and destination directories.</p>

  <hr>

  <h2>🧠 Features</h2>
  <ul>
    <li>Automatically detects over 100 file extensions across categories</li>
    <li>Supports recursive file search with <code>--recursive</code></li>
    <li><code>--dry-run</code> mode available for testing without moving files</li>
    <li>Logs all actions to <code>file_organizer.log</code></li>
    <li>Supports custom category extensions using <code>file_organizer_config.json</code></li>
    <li>Displays a summary report via GUI popup and console</li>
  </ul>

  <hr>

  <h2>🎞️ See It in Action</h2>
  <p>If you can't test it right now, here's a recorded video showing the program in action:</p>

  <p>🎥 video:
    <a href="https://github.com/iliaseymari/face-processing/raw/refs/heads/main/online-screen-recorder-2025-07-23--15-29-37.mp4">click on me!</a>
  </p>


