import shutil

def check_disk_usage():
    """Checks the disk usage of the root directory."""
    total, used, free = shutil.disk_usage("/")
    return f"Disk Usage: Used: {used // (2**30)} GB, Free: {free // (2**30)} GB"
