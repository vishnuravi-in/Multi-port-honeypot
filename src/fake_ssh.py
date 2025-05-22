import socket
import datetime

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 80         # Fake SSH port

# Set up logging
def log_connection(ip, port):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = conn.recv(100)
    log_entry = f"{timestamp} | IP: {ip} | Data: {data.decode(errors='ignore')} | Port: {port} | Action: Connection attempt\n"
    with open("honeypot.log", "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

# Start the fake service
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[*] Fake SSH service running on port {PORT}")
    while True:
        conn, addr = s.accept()
        log_connection(addr[0], PORT)
        conn.sendall(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\r\n")  # Fake SSH banner
        conn.close()