import tkinter as tk
from tkinter import ttk
from cpu.cpufreq import *

class CpuApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("CPU Tuner")

    self.min_hw, self.max_hw = get_hw_limits()

    self.min_var = tk.IntVar(value=self.min_hw)
    self.max_var = tk.IntVar(value=self.max_hw)

    #Apply clam theme
    self.style = ttk.Style(self)
    self.style.theme_use("clam")
  
    self.build_ui()
   
  def build_ui(self):
    # ---- Min freq ----
    tk.Label(self, text="Min Frequency").pack(anchor="w")
    self.min_value_lbl = ttk.Label(self, text=f"{self.format_freq(self.min_hw)}")
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
    tk.Label(self, text="Max Frequency").pack(anchor="w")
    self.max_value_lbl = ttk.Label(self, text=f"{self.format_freq(self.max_hw)}")
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
    tk.Label(self, text="Governor").pack(anchor="w")

    self.gov_var = tk.StringVar(value=get_current_governor())
    govs = get_available_governors()

    ttk.OptionMenu(self, self.gov_var, self.gov_var.get(), *govs).pack(fill="x")

    ttk.Button(self, text="Apply", command=self.apply).pack(pady=10)

  def update_min_label(self, value):
    self.min_value_lbl.config(text=self.format_freq(int(float(value))))

  def update_max_label(self, value):
    self.max_value_lbl.config(text=self.format_freq(int(float(value))))
  
  def format_freq(self, khz):
    return f"{khz / 1_000_000:.2f} GHz"

  def apply(self):
    set_limits(self.min_var.get(), self.max_var.get())
    set_governor(self.gov_var.get())

    
