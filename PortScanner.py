import argparse
import socket
import threading

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument("--domain", type=str, help="Enter the domain name")
parser.add_argument("--port", type=str, help="Enter the port range (i.e. --port 1-65000)")
parser.add_argument("--output", type=str, help="Specify the file name.")
args = parser.parse_args()

host = args.domain
portRange = args.port
fileName = args.output if args.output else f"{host}_ports"

# Get port range from string
def getPortRange(portRange):
    if portRange:
        return portRange.split("-")
    else:
        return ["1", "65535"]

# Thread-safe write lock
lock = threading.Lock()

# Scan a single port
def scan_port(host, port, fileName):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner_socket:
            scanner_socket.settimeout(1)
            result = scanner_socket.connect_ex((host, port))
            if result == 0:
                with lock:
                    with open(f"{fileName}.txt", "a") as file:
                        file.write(f"[+] Port {port} is OPEN\n")
                    print(f"[+] Port {port} is OPEN")
    except Exception:
        pass  # Handle exception silently

# Main logic
if host:
    portMin, portMax = int(getPortRange(portRange)[0]), int(getPortRange(portRange)[1])
    print(f"[+] Scanning {host} from port {portMin} to {portMax}")
    
    threads = []
    for port in range(portMin, portMax + 1):
        t = threading.Thread(target=scan_port, args=(host, port, fileName))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
else:
    print("[x] Please specify the domain name.")
