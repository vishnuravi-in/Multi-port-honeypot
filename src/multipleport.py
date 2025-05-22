import socket
import datetime
from threading import Thread

# Configuration
PORTS_SERVICES = {
    22: {"name": "SSH", "banner": b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\r\n"},
    80: {"name": "HTTP", "banner": b"HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\n\r\n"},
    3389: {"name": "RDP", "banner": b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00\x02\x1f\x08\x00\x02\x00\x00\x00"}
}

def log_connection(ip, port, data=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    service = PORTS_SERVICES.get(port, {}).get("name", str(port))
    
    log_entry = f"{timestamp} | Service: {service} | IP: {ip} | Port: {port}"
    if data:
        log_entry += f" | Data: {data.decode(errors='ignore')}"
    log_entry += "\n"
    
    with open("honeypot.log", "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

def handle_connection(conn, addr, port):
    try:
        # Send service-specific banner
        conn.sendall(PORTS_SERVICES[port]["banner"])
        
        # Receive data with timeout
        conn.settimeout(5.0)
        data = conn.recv(1024)  # Increased buffer size for HTTP
        
        log_connection(addr[0], port, data)
    except socket.timeout:
        log_connection(addr[0], port)
    finally:
        conn.close()

def start_honeypot(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen()
        print(f"[*] Fake {PORTS_SERVICES[port]['name']} service running on port {port}")
        
        while True:
            conn, addr = s.accept()
            Thread(target=handle_connection, args=(conn, addr, port)).start()

if __name__ == "__main__":
    # Start a thread for each service
    for port in PORTS_SERVICES:
        Thread(target=start_honeypot, args=(port,)).start()