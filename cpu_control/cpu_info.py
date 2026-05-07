import os

def get_cpu_info():
    model = "Unknown"
    logical = os.cpu_count() or 1
    physical_pairs = set()
    cpu_cores_field = None

    try:
        with open("/proc/cpuinfo", "r", encoding="utf-8") as f:
            phys_id = core_id = None
            for line in f:
                if not line.strip():
                    if phys_id is not None and core_id is not None:
                        physical_pairs.add((phys_id, core_id))
                    phys_id = core_id = None
                    continue
                key, _, val = line.partition(":")
                k = key.strip().lower()
                v = val.strip()

                if k == "model name" and model == "Unknown":
                    model = v
                elif k == "physical id":
                    phys_id = v
                elif k == "core id":
                    core_id = v
                elif k == "cpu cores" and cpu_cores_field is None:
                    try:
                        cpu_cores_field = int(v)
                    except ValueError:
                        pass
            if phys_id is not None and core_id is not None:
                physical_pairs.add((phys_id, core_id))
    except Exception:
        pass

    physical = len(physical_pairs) or 0
    return model, logical, int(physical)