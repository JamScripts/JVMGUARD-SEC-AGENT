import os
import platform
import socket
from datetime import datetime


def get_system_info():
    """Return basic information about the local system."""

    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        
        "current_time": datetime.now().astimezone().isoformat(),
    }


if __name__ == "__main__":
    print(get_system_info())
