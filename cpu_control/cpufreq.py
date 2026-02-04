import os
from .sysfs import cpu_cpufreq_paths, read, write

def _first_cpu():
  cpus = cpu_cpufreq_paths()
  if not cpus:
    raise RuntimeError("No CPUs with cpufreq support found")
  return cpus[0]


def get_hw_limits():
  cpu = _first_cpu()
  return (
    int(read(cpu + "/cpuinfo_min_freq")),
    int(read(cpu + "/cpuinfo_max_freq")),
  )


def get_available_governors():
  for cpu in cpu_cpufreq_paths():
    path = cpu + "/scaling_available_governors"
    if os.path.exists(path):
      return read(path).split()

  # Fallback: al menos mostrar el actual
  return [get_current_governor()]


def get_current_governor():
    cpu = _first_cpu()
    return read(cpu + "/scaling_governor")


def set_governor(governor):
  for cpu in cpu_cpufreq_paths():
    try:
      write(cpu + "/scaling_governor", governor)
    except PermissionError:
      pass


def set_limits(min_freq, max_freq):
  if min_freq > max_freq:
    raise ValueError("min_freq > max_freq")

  print(cpu_cpufreq_paths())

  for cpu in cpu_cpufreq_paths():
    # Leer valores actuales
    current_min = int(read(cpu + "/scaling_min_freq"))
    current_max = int(read(cpu + "/scaling_max_freq"))
    
    print(f"CPU: {cpu}")
    print(f" Current min: {current_min}, max: {current_max}")
    print(f" Setting min: {min_freq}, max: {max_freq}") 
