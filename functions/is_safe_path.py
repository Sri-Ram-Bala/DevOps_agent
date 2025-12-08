import os

# --- SECURITY LAYER (The "Guardrails") ---
ALLOWED_LOG_DIR = "/var/log"

def is_safe_path(filepath: str) -> bool:
    """
    Security Check: Prevents 'Path Traversal' attacks.
    Ensures the agent only reads files inside /var/log.
    """
    # Resolve '..' to get the real absolute path
    absolute_path = os.path.abspath(filepath)
    # Check if it starts with the allowed directory
    return absolute_path.startswith(ALLOWED_LOG_DIR)