#!/bin/python
import sys
import socket
import threading
import nmap
import subprocess

# Lists and variables
open_ports = []

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 4:
    print("Syntax: python3 port_scanner.py <target_host> <Port_min_range> <Port_max_range>")
    sys.exit(1)

# Resolve the target host's IP address and set the port range
try:
    IP = socket.gethostbyname(sys.argv[1])
    port_min = int(sys.argv[2])
    port_max = int(sys.argv[3])

except socket.gaierror:
    print("Error: Hostname cannot be resolved.")
    sys.exit(1)

# banner
print("-" * 60)
print("Port Scanner - Scan ports on a target host")
print("Target: " + IP)
print("Scanning ports from {} to {}".format(port_min, port_max))
print("-" * 60)

# Scan a range of ports
def scan_ports(IP, ports):
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((IP, port))
        if result == 0:
            open_ports.append(port)
            print("Port {} is open".format(port))
        s.close()

# Nmap Scan for all the Open ports.
def nmap_open_ports(IP, open_ports):
    # Display Nmap results on terminal


    for port in open_ports:
    	print("-" * 40)
    	print(f"Nmap Scan for port {port}")
    	print("Target: " + IP)
    	print("-" * 40)
    	nmap_command = f'nmap {IP} -p {port} -T4 -A'
    	nmap_result = subprocess.check_output(nmap_command, shell=True, text=True)
    	print(nmap_result)


# Threading and running the scan concurrently
def run_port_scans(IP, thread_count, port_min, port_max):
    port_range = list(range(port_min, port_max))
    chunk_size = len(port_range) // thread_count

    threads = []
    for i in range(thread_count):
        start = i * chunk_size
        end = start + chunk_size
        thread = threading.Thread(target=scan_ports, args=(IP, port_range[start:end]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Main
try:
    run_port_scans(IP, 24, port_min, port_max)
    nmap_open_ports(IP, open_ports)


except KeyboardInterrupt:
    print("Exiting the program")
    sys.exit()

except socket.error:
    print("Error: Couldn't connect to the target IP")
    sys.exit()
