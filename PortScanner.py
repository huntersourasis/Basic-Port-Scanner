import argparse
import socket
parser = argparse.ArgumentParser()
parser.add_argument("--domain" , type=str  , help="Enter the domain name")
parser.add_argument("--port" , type=str , help="Enter the port range (i.e. --port 1-65000)")
parser.add_argument("--output" , type=str , help="Speacify the file name.")
args = parser.parse_args()
host  = args.domain
portRange = args.port
fileName = args.output if args.output != None else f"{host}_ports"
def getPortRange(portRange):
    if portRange != None:
        return portRange.split("-")
    else :
        return ["1" , "65535"]
if host != None:
    portMin = int(getPortRange(portRange)[0])
    portMax = int(getPortRange(portRange)[1])
    print(f"[+] Scanning {host} from port {portMin} to {portMax}")
    while portMin <= portMax:
        scanner_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        scanner_socket.settimeout(1)
        res = scanner_socket.connect_ex((host , portMin))
        if res == 0 :
            with open(f"{fileName}.txt" , "a") as file :
                file.write(f"[+] Port {portMin} is OPEN \n")
            print(f"[+] Port {portMin} is OPEN")
        portMin+=1
        scanner_socket.close()
else :
    print("[x] Please speacify the domain name.")
