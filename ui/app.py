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
    tk.Label(self, text="Min Frequency (kHz)").pack()
    ttk.Scale(self, from_=self.min_hw, to=self.max_hw,             orient="horizontal", variable=self.min_var).pack(fill="x")

    tk.Label(self, text="Max Frequency (kHz)").pack()
    ttk.Scale(self, from_=self.min_hw, to=self.max_hw,             orient="horizontal", variable=self.max_var).pack(fill="x")
    
    tk.Label(self, text="Governor").pack()
    self.gov_var = tk.StringVar(value=get_current_governor())
    govs = get_available_governors()

    ttk.OptionMenu(self, self.gov_var, self.gov_var.get(), *govs).pack()

    ttk.Button(self, text="Apply", command=self.apply).pack(pady=10)

  def apply(self):
    set_limits(self.min_var.get(), self.max_var.get())
    set_governor(self.gov_var.get())

    
