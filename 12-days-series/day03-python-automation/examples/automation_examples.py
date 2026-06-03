#!/usr/bin/env python3
"""
Python Automation Examples for Infrastructure Tasks
Demonstrates common automation patterns.
"""

import os
import subprocess
import json
from datetime import datetime
from typing import List, Dict

# =============================================================================
# 1. SYSTEM MONITORING
# =============================================================================


def check_disk_usage(threshold: int = 80) -> Dict[str, any]:
    """Check disk usage and alert if above threshold."""
    import shutil

    total, used, free = shutil.disk_usage("/")
    percent_used = (used / total) * 100

    result = {
        "total_gb": round(total / (1024**3), 2),
        "used_gb": round(used / (1024**3), 2),
        "free_gb": round(free / (1024**3), 2),
        "percent_used": round(percent_used, 2),
        "alert": percent_used > threshold,
    }

    return result


def check_memory_usage() -> Dict[str, any]:
    """Check system memory usage."""
    try:
        with open("/proc/meminfo", "r") as f:
            meminfo = {}
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = int(parts[1].strip().split()[0])
                    meminfo[key] = value

        total = meminfo.get("MemTotal", 0)
        available = meminfo.get("MemAvailable", 0)
        used = total - available

        return {
            "total_mb": round(total / 1024, 2),
            "used_mb": round(used / 1024, 2),
            "available_mb": round(available / 1024, 2),
            "percent_used": round((used / total) * 100, 2),
        }
    except Exception as e:
        return {"error": str(e)}


# =============================================================================
# 2. FILE OPERATIONS
# =============================================================================


def find_large_files(directory: str, min_size_mb: int = 100) -> List[Dict]:
    """Find files larger than specified size."""
    large_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                if size >= min_size_mb * 1024 * 1024:
                    large_files.append(
                        {
                            "path": filepath,
                            "size_mb": round(size / (1024 * 1024), 2),
                            "modified": datetime.fromtimestamp(
                                os.path.getmtime(filepath)
                            ).isoformat(),
                        }
                    )
            except (PermissionError, FileNotFoundError):
                continue

    return sorted(large_files, key=lambda x: x["size_mb"], reverse=True)


def cleanup_old_files(directory: str, days_old: int = 30) -> Dict[str, int]:
    """Clean up files older than specified days."""
    from datetime import timedelta

    cutoff = datetime.now() - timedelta(days=days_old)
    stats = {"deleted": 0, "skipped": 0, "errors": 0}

    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mtime < cutoff:
                    os.remove(filepath)
                    stats["deleted"] += 1
                else:
                    stats["skipped"] += 1
            except Exception:
                stats["errors"] += 1

    return stats


# =============================================================================
# 3. PROCESS MANAGEMENT
# =============================================================================


def get_process_info(process_name: str) -> List[Dict]:
    """Get information about running processes."""
    processes = []

    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)

        for line in result.stdout.split("\n")[1:]:
            if process_name.lower() in line.lower() and line.strip():
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    processes.append(
                        {
                            "user": parts[0],
                            "pid": int(parts[1]),
                            "cpu": float(parts[2]),
                            "memory": float(parts[3]),
                            "command": parts[10],
                        }
                    )
    except Exception as e:
        print(f"Error: {e}")

    return processes


def restart_service(service_name: str) -> bool:
    """Restart a system service (requires sudo)."""
    try:
        # For systemd systems
        subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        # Try service command for older systems
        try:
            subprocess.run(["sudo", "service", service_name, "restart"], check=True)
            return True
        except:
            return False


# =============================================================================
# 4. NETWORK OPERATIONS
# =============================================================================


def check_port_open(host: str, port: int) -> bool:
    """Check if a port is open on a host."""
    import socket

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def ping_host(host: str, count: int = 3) -> Dict[str, any]:
    """Ping a host and return statistics."""
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), host],
            capture_output=True,
            text=True,
            timeout=count * 2 + 5,
        )

        output = result.stdout
        success = result.returncode == 0

        # Parse packet loss
        loss = "100%"
        for line in output.split("\n"):
            if "% packet loss" in line:
                loss = line.split("% packet loss")[0].split(",")[-1].strip()
                break

        return {"success": success, "packet_loss": loss, "output": output.strip()}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# 5. LOG ANALYSIS
# =============================================================================


def analyze_log_file(log_path: str, lines: int = 100) -> Dict[str, any]:
    """Analyze recent log entries."""
    try:
        with open(log_path, "r") as f:
            all_lines = f.readlines()
            recent = all_lines[-lines:] if len(all_lines) > lines else all_lines

        # Count error levels
        errors = sum(1 for l in recent if "ERROR" in l or "error" in l)
        warnings = sum(1 for l in recent if "WARN" in l or "warn" in l)
        info = sum(1 for l in recent if "INFO" in l or "info" in l)

        return {
            "total_lines": len(recent),
            "errors": errors,
            "warnings": warnings,
            "info": info,
            "error_rate": round((errors / len(recent)) * 100, 2) if recent else 0,
        }
    except Exception as e:
        return {"error": str(e)}


def search_logs(log_path: str, pattern: str) -> List[str]:
    """Search for pattern in log file."""
    matches = []

    try:
        with open(log_path, "r") as f:
            for line in f:
                if pattern.lower() in line.lower():
                    matches.append(line.strip())
    except Exception as e:
        print(f"Error: {e}")

    return matches


# =============================================================================
# 6. BACKUP OPERATIONS
# =============================================================================


def create_backup(source_dir: str, backup_dir: str) -> Dict[str, any]:
    """Create a timestamped backup of a directory."""
    import tarfile

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.tar.gz"
    backup_path = os.path.join(backup_dir, backup_name)

    os.makedirs(backup_dir, exist_ok=True)

    try:
        with tarfile.open(backup_path, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

        size = os.path.getsize(backup_path)

        return {
            "success": True,
            "backup_path": backup_path,
            "size_mb": round(size / (1024 * 1024), 2),
            "timestamp": timestamp,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PYTHON AUTOMATION EXAMPLES")
    print("=" * 70)

    # System monitoring
    print("\n1. DISK USAGE")
    print("-" * 40)
    disk = check_disk_usage()
    print(json.dumps(disk, indent=2))

    print("\n2. MEMORY USAGE")
    print("-" * 40)
    mem = check_memory_usage()
    print(json.dumps(mem, indent=2))

    # File operations
    print("\n3. FIND LARGE FILES (in /tmp)")
    print("-" * 40)
    large = find_large_files("/tmp", min_size_mb=10)
    print(f"Found {len(large)} large files")
    if large:
        print(json.dumps(large[:3], indent=2))

    # Process management
    print("\n4. PROCESS INFO (python)")
    print("-" * 40)
    procs = get_process_info("python")
    print(f"Found {len(procs)} python processes")

    # Network
    print("\n5. PING GOOGLE")
    print("-" * 40)
    ping_result = ping_host("8.8.8.8")
    print(f"Success: {ping_result.get('success')}")

    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)
