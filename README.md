<body>
  <h1>ronEZexeLauncher</h1>
  <p><strong>ronEZexeLauncher</strong> is a lightweight Python GUI tool that lets you launch any <code>.exe</code> file multiple times — perfect for testing, multi-client sessions, or custom automation.</p>

  <h2>🚀 Features</h2>
  <ul>
    <li>Select and save any executable path</li>
    <li>Optional launch argument (e.g. <code>-argument</code> for exe)</li>
    <li>Specify number of instances (default: <code>2</code>)</li>
    <li>Toggleable Settings panel</li>
    <li>Automatically saves your config (path, argument, instances)</li>
    <li>Runs from its own directory (supports relative/absolute paths)</li>
    <li>Windows UAC auto-elevation for admin rights</li>
    <li>Simple Tkinter interface with Start & Stop controls</li>
  </ul>

  <h2>🖥 How to Use</h2>
  <ol>
    <li>Run the launcher: <code>python ronEZexeLauncher.py</code></li>
    <li>Click <strong>"📂 Browse .exe location"</strong> to select your target <code>.exe</code> file</li>
    <li>Toggle <strong>⚙️ Settings</strong> to:
      <ul>
        <li>Add an optional launch argument</li>
        <li>Set number of instances to launch</li>
      </ul>
    </li>
    <li>Press <strong>Start Launching</strong> to fire up your instances</li>
    <li>You can cancel midway using the <strong>Stop</strong> button</li>
  </ol>

  <h2>💡 Requirements</h2>
  <ul>
    <li>Python 3.x</li>
    <li>Windows OS</li>
    <li>Admin privileges (auto-elevated on launch)</li>
  </ul>

  <h2>📄 Config</h2>
  <p>Settings are saved in <code>launcher_config.txt</code> in the same folder:</p>
  <pre>
C:\Path\To\Notepad.exe
argument
5
  </pre>

  <h2>📦 Packaging (Optional)</h2>
  <p>Use <code>pyinstaller</code> to turn it into a <code>.exe</code>:</p>
  <pre>
pyinstaller --noconsole --onefile ronEZexeLauncher.py
  </pre>

</body>
</html>
