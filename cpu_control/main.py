from cpu_control.app import CpuApp
from tkinter import messagebox, Tk
from cpu_control.cpufreq import cpu_cpufreq_paths

def main():
    cpus = cpu_cpufreq_paths()
    if not cpus:
        root = Tk()
        root.withdraw()
        messagebox.showerror(
            "CPU Control Error",
            "No CPUs with cpufreq support found.\n"
            "This usually happens in virtual machines.\n"
            "Please run this app on real hardware."
        )
        return
    app = CpuApp()
    app.mainloop()

if __name__ == "__main__":
    main()
