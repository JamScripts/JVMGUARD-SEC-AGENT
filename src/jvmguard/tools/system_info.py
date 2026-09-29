import platform
import socket
from datetime import datetime


def get_system_info() -> dict[str, str]:
    """Return basic information about the local system."""

    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "current_time": datetime.now().astimezone().isoformat(),
    }
