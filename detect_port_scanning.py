import re
import subprocess
import time
from datetime import datetime, timedelta

# File to store blocked IPs
BLOCKED_IP_FILE = "blocked_ip_list.txt"

# Dictionary to track IP activity and block times
ip_activity = {}
blocked_ips = {}
BLOCK_DURATION = timedelta(minutes=30)
THRESHOLD = 5  # Number of suspicious activities before blocking

def parse_tcpdump_line(line):
    """Parses a tcpdump line and extracts the source IP."""
    match = re.search(r"(\d+\.\d+\.\d+\.\d+)(?=\.\d+ >)", line)
    if match:
        return match.group(1)
    return None

def block_ip(ip):
    """Blocks an IP by adding it to the blocked list."""
    blocked_ips[ip] = datetime.now() + BLOCK_DURATION
    with open(BLOCKED_IP_FILE, "a") as f:
        f.write(f"{ip}\n")
    print(f"Blocked IP: {ip} for {BLOCK_DURATION} minutes.")

def unblock_ip(ip):
    """Unblocks an IP by removing it from the blocked list."""
    if ip in blocked_ips:
        del blocked_ips[ip]
        print(f"Unblocked IP: {ip}")

def cleanup_blocked_ips():
    """Unblocks IPs whose block duration has expired."""
    now = datetime.now()
    expired_ips = [ip for ip, unblock_time in blocked_ips.items() if now >= unblock_time]
    for ip in expired_ips:
        unblock_ip(ip)
    # Update the file
    with open(BLOCKED_IP_FILE, "w") as f:
        for ip in blocked_ips:
            f.write(f"{ip}\n")

def process_tcpdump_line(line):
    """Processes a single tcpdump line."""
    ip = parse_tcpdump_line(line)
    if ip:
        if ip in blocked_ips:
            return  # Ignore already blocked IPs

        ip_activity[ip] = ip_activity.get(ip, 0) + 1
        if ip_activity[ip] >= THRESHOLD:
            block_ip(ip)
            del ip_activity[ip]  # Reset activity count after blocking

def monitor_tcpdump():
    """Monitors tcpdump output for suspicious traffic."""
    print("Monitoring tcpdump for port scanning...")
    try:
        process = subprocess.Popen(
            ["tcpdump", "-i", "eth0", "tcp[tcpflags] & tcp-syn != 0", "-n"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in process.stdout:
            process_tcpdump_line(line)
            cleanup_blocked_ips()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        process.terminate()

if __name__ == "__main__":
    monitor_tcpdump()
