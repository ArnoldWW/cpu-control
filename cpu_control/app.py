import subprocess
import sys
import math
import tkinter as tk
from tkinter import ttk
from .cpufreq import *
from .sysfs import read, cpu_cpufreq_paths


class CpuApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("CPU Control")
    self.geometry("500x500")

    # Hardware limits
    min_hw_raw, max_hw_raw = get_hw_limits()
    self.min_hw = math.floor(min_hw_raw / 100000) * 100000
    self.max_hw = math.floor(max_hw_raw / 100000) * 100000
    
    # Current freq
    first_cpu = cpu_cpufreq_paths()[0]
    self.current_min = int(read(first_cpu + "/scaling_min_freq"))
    self.current_max = int(read(first_cpu + "/scaling_max_freq"))

    # Current governor
    self.current_gov = get_current_governor()

    # Variables for sliders
    self.min_var = tk.IntVar(value=self.current_min)
    self.max_var = tk.IntVar(value=self.current_max)

    # Apply clam theme
    self.style = ttk.Style(self)
    self.style.theme_use("clam")

    self.build_ui()
   
  def build_ui(self):
    # ---- Current Status ----
    ttk.Label(self, text="Current Settings", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(10, 5))
    
    
    ttk.Label(self, text=f"Min: {self.format_freq(self.current_min)}").pack(anchor="w")
    ttk.Label(self, text=f"Max: {self.format_freq(self.current_max)}").pack(anchor="w")
    ttk.Label(self, text=f"Governor: {self.current_gov}").pack(anchor="w")
    
    ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)

    # ---- Min freq ----
    ttk.Label(self, text="Min Frequency", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
    self.min_value_lbl = ttk.Label(self, text=f"{self.format_freq(self.min_var.get())}")
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
    self.max_value_lbl = ttk.Label(self, text=f"{self.format_freq(self.max_var.get())}")
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

    # --- Apply Button ----
    ttk.Button(self, text="Apply", command=self.apply).pack()

  def update_min_label(self, value):
    print("Update min label to " + str(value))
    min_value = int(float(value))
    
    # Avoid min being greater than max
    if min_value > self.max_var.get():
        min_value = self.max_var.get()
        self.min_var.set(min_value)
    
    self.min_value_lbl.config(text=self.format_freq(min_value))

  def update_max_label(self, value):
    max_value = int(float(value))
    
    # Avoid max being less than min
    if max_value < self.min_var.get():
        max_value = self.min_var.get()
        self.max_var.set(max_value)
    
    self.max_value_lbl.config(text=self.format_freq(max_value))
  
  def format_freq(self, khz):
    return f"{khz / 1_000_000:.2f} GHz"

  def apply(self):
    import os
    helper_path = os.path.join(os.path.dirname(__file__), "apply.py")

    print("Apply min" + str(self.min_var.get()))

    cmd = [
      "pkexec",
      sys.executable,
      helper_path,
      str(self.min_var.get()),
      str(self.max_var.get()),
      self.gov_var.get(),
    ]

    subprocess.run(cmd)
    self.reload_ui()

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

    
