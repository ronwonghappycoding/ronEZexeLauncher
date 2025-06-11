import subprocess
import time
import os
import sys
import ctypes
import threading
import tkinter as tk
from tkinter import filedialog

CONFIG_FILE = "launcher_config.txt"
stop_flag = False
exe_path = None

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate():
    if not is_admin():
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()

def save_config(path, argument, instances):
    with open(CONFIG_FILE, "w") as f:
        f.write(f"{path}\n{argument}\n{instances}")

def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            lines = f.read().splitlines()
            path = lines[0] if len(lines) > 0 else ""
            argument = lines[1] if len(lines) > 1 else ""
            instances = lines[2] if len(lines) > 2 else "2"
            if os.path.isfile(path):
                return path, argument, instances
            else:
                os.remove(CONFIG_FILE)
    return None, "", "2"

def browse_file():
    global exe_path
    path = filedialog.askopenfilename(title="Select .exe", filetypes=[("Executable Files", "*.exe")])
    if path:
        exe_path = path
        save_config(exe_path, arg_entry.get().strip(), instance_entry.get().strip())
        exe_label.config(text=f"Selected: {os.path.basename(exe_path)}")
        log_var.set("✅ Path saved. Ready to launch!")

def launch_exes():
    global stop_flag
    arg = arg_entry.get().strip()

    try:
        num_instances = int(instance_entry.get())
    except ValueError:
        log_var.set("⚠️ Invalid number of instances.")
        return

    if not exe_path:
        log_var.set("⚠️ Please select an executable first.")
        return

    save_config(exe_path, arg, str(num_instances))
    command = [exe_path] if not arg else [exe_path, arg]

    for i in range(num_instances):
        if stop_flag:
            log_var.set("🚫 Launch cancelled.")
            return
        log_var.set(f"🚀 Launching instance {i + 1}/{num_instances}")
        try:
            subprocess.Popen(command, cwd=os.path.dirname(exe_path))
        except Exception as e:
            log_var.set(f"❌ Launch failed: {e}")
            return
        time.sleep(12)

    log_var.set("🎉 All instances launched!")

def start_launch():
    global stop_flag
    stop_flag = False
    threading.Thread(target=launch_exes, daemon=True).start()

def stop_launch():
    global stop_flag
    stop_flag = True

def start_gui():
    global log_var, exe_label, exe_path, arg_entry, instance_entry, settings_frame

    def toggle_settings():
        if settings_frame.winfo_ismapped():
            settings_frame.pack_forget()
        else:
            settings_frame.pack(pady=(5, 0))

    def on_update(*args):
        if exe_path:
            save_config(exe_path, arg_entry.get().strip(), instance_entry.get().strip())

    window = tk.Tk()
    window.title("ronEZexeLauncher")
    window.geometry("320x340+0+0")
    window.resizable(False, False)

    tk.Button(window, text="📂 Browse .exe location", width=20, height=2, command=browse_file).pack(pady=(15, 5))
    exe_label = tk.Label(window, text="No file selected", font=("Segoe UI", 9))
    exe_label.pack()

    tk.Button(window, text="⚙️ Settings", command=lambda: [toggle_settings(), on_update()]).pack(pady=(10, 0))

    settings_frame = tk.Frame(window)

    tk.Label(settings_frame, text="argument (optional):", font=("Segoe UI", 10)).pack()
    arg_entry = tk.Entry(settings_frame, width=30)
    arg_entry.pack(pady=5)

    tk.Label(settings_frame, text="Number of instances:", font=("Segoe UI", 10)).pack()
    instance_entry = tk.Entry(settings_frame, width=10)
    instance_entry.pack(pady=5)

    arg_entry.bind("<FocusOut>", on_update)
    arg_entry.bind("<Return>", on_update)
    instance_entry.bind("<FocusOut>", on_update)
    instance_entry.bind("<Return>", on_update)

    log_var = tk.StringVar()
    log_var.set("Location and settings must be set.")
    tk.Label(window, textvariable=log_var, font=("Segoe UI", 10)).pack(pady=(15, 5))

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Stop", width=20, height=2, command=stop_launch).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Start Launching", width=20, height=2, command=start_launch).pack(side="left", padx=10)

    exe_path, saved_arg, saved_instances = load_config()
    arg_entry.insert(0, saved_arg)
    instance_entry.insert(0, saved_instances)
    if exe_path:
        exe_label.config(text=f"Last used: {os.path.basename(exe_path)}")
    else:
        exe_label.config(text="No file selected (saved path not found)")
        log_var.set("⚠️ Saved path not found. Please browse again.")

    window.mainloop()

if __name__ == "__main__":
    elevate()
    start_gui()
