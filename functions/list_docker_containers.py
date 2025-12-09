import subprocess

def list_docker_containers():
    """
    Lists active Docker containers and their status.
    """
    try:
        # We use subprocess to call the docker CLI
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "table {{.Names}}\t{{.Status}}"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return "Error: Docker is not running or permission denied. Try 'sudo'."
    except FileNotFoundError:
        return "Error: Docker is not installed."