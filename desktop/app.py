
#!/usr/bin/env python3

import subprocess
import tkinter as tk
from tkinter import ttk


APP_TITLE = "tr4mpass Desktop"
BACKGROUND = "#111318"
PANEL = "#1b1e25"
ACCENT = "#e53935"
TEXT = "#f2f2f2"
MUTED = "#a5a9b3"


def run_read_only(command):
    """Run a device-information command without making device changes."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip() or "No information returned."
        return result.stderr.strip() or "No device information available."
    except FileNotFoundError:
        return f"Required command not installed: {command[0]}"
    except subprocess.TimeoutExpired:
        return "The command timed out. Check the USB connection."


class DeviceApp:
    def __init__(self, root):
        self.root = root
        root.title(APP_TITLE)
        root.geometry("760x540")
        root.minsize(600, 440)
        root.configure(bg=BACKGROUND)

        header = tk.Frame(root, bg=BACKGROUND, padx=24, pady=20)
        header.pack(fill="x")

        tk.Label(
            header,
            text="tr4mpass",
            font=("TkDefaultFont", 24, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="DEVICE DIAGNOSTICS",
            font=("TkDefaultFont", 10, "bold"),
            fg=ACCENT,
            bg=BACKGROUND,
        ).pack(anchor="w", pady=(4, 0))

        panel = tk.Frame(root, bg=PANEL, padx=18, pady=18)
        panel.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        tk.Label(
            panel,
            text="Connected device information",
            font=("TkDefaultFont", 13, "bold"),
            fg=TEXT,
            bg=PANEL,
        ).pack(anchor="w")

        tk.Label(
            panel,
            text="Connect your device using USB, then refresh.",
            fg=MUTED,
            bg=PANEL,
        ).pack(anchor="w", pady=(6, 14))

        actions = tk.Frame(panel, bg=PANEL)
        actions.pack(anchor="w", pady=(0, 14))

        ttk.Button(
            actions,
            text="Refresh USB devices",
            command=self.refresh_usb,
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            actions,
            text="Read device information",
            command=self.read_device,
        ).pack(side="left")

        self.output = tk.Text(
            panel,
            bg="#0b0d11",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            wrap="word",
            font=("TkFixedFont", 10),
            padx=12,
            pady=12,
        )
        self.output.pack(fill="both", expand=True)
        self.show_text("Connect a device and select an action.")

        self.status = tk.StringVar(value="Ready")
        tk.Label(
            root,
            textvariable=self.status,
            bg=BACKGROUND,
            fg=MUTED,
            anchor="w",
            padx=24,
            pady=8,
        ).pack(fill="x", side="bottom")

    def show_text(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def refresh_usb(self):
        self.status.set("Checking USB devices...")
        result = run_read_only(["lsusb"])
        self.show_text(result)
        self.status.set("USB scan finished")

    def read_device(self):
        self.status.set("Reading device information...")
        result = run_read_only(["ideviceinfo"])
        self.show_text(result)
        self.status.set("Device information request finished")


def main():
    root = tk.Tk()
    DeviceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
      
