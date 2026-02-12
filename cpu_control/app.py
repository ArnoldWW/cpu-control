import subprocess
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from .cpufreq import get_hw_limits, get_current_governor, get_available_governors
from .sysfs import read, cpu_cpufreq_paths


class CpuApp(tk.Tk):
    def __init__(self):
        super().__init__(className="cpu-control")
        self.title("CPU Control")
        self.geometry("500x500")

        # add icon to the window
        icon_path = os.path.join(os.path.dirname(__file__), "assets/icon.png")
        if os.path.exists(icon_path):
            self.iconphoto(True, tk.PhotoImage(file=icon_path))

        # Hardware limits (rounded down to nearest 10 MHz)
        min_hw_raw, max_hw_raw = get_hw_limits()
        self.min_hw = int(min_hw_raw / 10_000) * 10_000
        self.max_hw = int(max_hw_raw / 10_000) * 10_000

        print(f"Hardware limits: min={self.min_hw}, max={self.max_hw}")

        # Current frequency settings (rounded down to nearest 10 MHz)
        first_cpu = cpu_cpufreq_paths()[0]
        self.current_min = int(
            int(read(first_cpu + "/scaling_min_freq")) / 10_000) * 10_000
        self.current_max = int(
            int(read(first_cpu + "/scaling_max_freq")) / 10_000) * 10_000

        print(f"Current settings: min={self.current_min}, max={self.current_max}")

        # Current governor
        self.current_gov = get_current_governor()

        # Variables for sliders
        self.min_var = tk.IntVar(value=self.current_min)
        self.max_var = tk.IntVar(value=self.current_max)

        print(f"Initial slider values: min={self.min_var.get()}, max={self.max_var.get()}")

        # Apply clam theme
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.build_ui()
    
    def build_ui(self):
        # ---- Current Status ----
        ttk.Label(self, text="Current Settings", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(10, 5))
             
        ttk.Label(self, text=f"Min: {self.current_min} KHz ~ {self.format_freq_ghz(self.current_min)}").pack(anchor="w")
        ttk.Label(self, text=f"Max: {self.current_max} KHz ~ {self.format_freq_ghz(self.current_max)}").pack(anchor="w")
        ttk.Label(self, text=f"Governor: {self.current_gov}").pack(anchor="w")
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

        # ---- Min freq ----
        ttk.Label(self, text="Min Frequency", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.min_value_lbl = ttk.Label(self, text=f"{self.format_freq_ghz(self.min_var.get())}")
        self.min_value_lbl.pack(anchor="e")

        ttk.Scale(
            self,
            from_=self.min_hw,
            to=self.max_hw,
            orient="horizontal",
            variable=self.min_var,
            command=self.update_min_label
        ).pack(fill="x")

        # ---- Max freq ----
        ttk.Label(self, text="Max Frequency", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.max_value_lbl = ttk.Label(self, text=f"{self.format_freq_ghz(self.max_var.get())}")
        self.max_value_lbl.pack(anchor="e")

        ttk.Scale(
            self,
            from_=self.min_hw,
            to=self.max_hw,
            orient="horizontal",
            variable=self.max_var,
            command=self.update_max_label
        ).pack(fill="x")

        # ---- Governor ----
        ttk.Label(self, text="Governor", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")

        self.gov_var = tk.StringVar(value=get_current_governor())
        govs = get_available_governors()

        ttk.OptionMenu(self, self.gov_var, self.gov_var.get(), *govs).pack(fill="x")

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=20)

        # --- Buttons ----
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=5)
        
        ttk.Button(button_frame, text="Apply", command=self.apply).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(button_frame, text="Save Config", command=self.save_config).pack(side="left", expand=True, fill="x", padx=(5, 0))
        ttk.Button(button_frame, text="Remove Service", command=self.remove_service).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def update_min_label(self, value):
        print("Min slider value: " + str(int(float(value))))  
        round_min_value = self.round_freq_nearest_10_mhz(int(float(value)))
        round_max_value = self.round_freq_nearest_10_mhz(self.max_var.get())
        print("Rounded min value: " + str(round_min_value))
        
        # Avoid min being greater than max
        if round_min_value > round_max_value:
            round_min_value = round_max_value
            self.min_var.set(round_min_value)
        
        self.min_value_lbl.config(text=self.format_freq_ghz(round_min_value))

    def update_max_label(self, value):
        round_max_value = self.round_freq_nearest_10_mhz(int(float(value)))
        round_min_value = self.round_freq_nearest_10_mhz(self.min_var.get())
        print("Rounded max value: " + str(round_max_value))

        # Avoid max being less than min
        if round_max_value < round_min_value:
            round_max_value = round_min_value
            self.max_var.set(round_max_value)

        self.max_value_lbl.config(text=self.format_freq_ghz(round_max_value))
    
    # Helper to format frequency in GHz
    def format_freq_ghz(self, khz):
        return f"{khz / 1_000_000:.2f} GHz"
    
    # round to down nearest 10 MHz (10,000 KHz ~ 0.01 GHz)
    def round_freq_nearest_10_mhz(self, khz):
        return int(khz / 10_000) * 10_000

    def apply(self):
        """Apply current settings without saving"""
        helper_path = os.path.join(os.path.dirname(__file__), "apply.py")

        # Round to down nearest 10 MHz (10,000 KHz)
        min_value = self.round_freq_nearest_10_mhz(self.min_var.get())
        max_value = self.round_freq_nearest_10_mhz(self.max_var.get())

        self.min_var.set(min_value)
        self.max_var.set(max_value)

        print("Apply min" + str(min_value))
        print("Apply max" + str(max_value))

        cmd = [
            "pkexec",
            sys.executable,
            helper_path,
            str(min_value),
            str(max_value),
            self.gov_var.get(),
        ]

        subprocess.run(cmd)
        self.reload_ui()

    def save_config(self):
        """Save current configuration and install systemd service"""
        helper_path = os.path.join(os.path.dirname(__file__), "install_service.py")
        
        min_value_to_save = self.round_freq_nearest_10_mhz(self.min_var.get())
        max_value_to_save = self.round_freq_nearest_10_mhz(self.max_var.get())

        cmd = [
            "pkexec",
            sys.executable,
            helper_path,
            str(min_value_to_save),
            str(max_value_to_save),
            self.gov_var.get(),
        ]
        
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo(
                "Success",
                "Configuration saved!\nSystemd service installed and enabled.\nSettings will be applied on next boot."
            )
        except subprocess.CalledProcessError as e: 
            print(f"Error details: {e.stderr or e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    def remove_service(self):
        """Remove the systemd service"""
        helper_path = os.path.join(os.path.dirname(__file__), 
                                   "remove_service.py")
        try:
            subprocess.run(
                ["pkexec", sys.executable, helper_path],
                check=True,
                capture_output=True,
                text=True
            )
            messagebox.showinfo("Success", "Systemd service removed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", "Failed to remove service, maybe the service doesn't exist")
            print(f"Error details: {e.stderr or e}")
    
    def reload_ui(self):
        # Destroy current widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Update current values
        first_cpu = cpu_cpufreq_paths()[0]
        self.current_min = int(read(first_cpu + "/scaling_min_freq"))
        self.current_max = int(read(first_cpu + "/scaling_max_freq"))

        # Current governor
        self.current_gov = get_current_governor()

        # Rebuild UI
        self.build_ui()