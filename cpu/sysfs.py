import glob
import os

CPU_PATH = "/sys/devices/system/cpu/"

def cpu_cpufreq_paths():
  paths = []
  for cpu in glob.glob(CPU_PATH + "cpu[0-9]*"):
    cpufreq = os.path.join(cpu, "cpufreq")
    gov = os.path.join(cpufreq, "scaling_governor")

    if os.path.isdir(cpufreq) and os.path.exists(gov):
        paths.append(cpufreq)

    return paths

def read(path):
  with open(path, "r") as f:
    return f.read().strip()

def write(path, value):
  with open(path, "w") as f:
    f.write(str(value))
