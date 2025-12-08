import os
from functions.is_safe_path import is_safe_path


# --- TOOLS (The "Hands") ---

def read_system_log(log_type: str = "syslog"):
    """
    Reads the last 30 lines of a Linux system log.
    Args:
        log_type: 'syslog', 'auth', or 'kern'.
    """
    log_map = {
        "syslog": "/var/log/syslog",
        "auth": "/var/log/auth.log",
        "kern": "/var/log/kern.log"
    }
    
    filepath = log_map.get(log_type, "/var/log/syslog")

    # 🔒 Security Check
    if not is_safe_path(filepath):
        return f"⛔ SECURITY ALERT: Access to {filepath} is blocked."

    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' not found."
    
    if not os.access(filepath, os.R_OK):
        return f"⛔ PERMISSION DENIED: Run with 'sudo' to read {filepath}."

    try:
        with open(filepath, "r") as f:
            lines = f.readlines()[-30:]
            return "".join(lines)
    except Exception as e:
        return f"Error reading log: {str(e)}"