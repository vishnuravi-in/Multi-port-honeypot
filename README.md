# Honeypot Project
A multi-port deception service detecting unauthorized access attempts.

## Features
- Fake SSH/HTTP/RDP services
- Attack logging with GeoIP
- Real-time Telegram alerts

## Setup
```bash
pip3 install -r requirements.txt
python3 src/fake_ssh.py
python3 src/multipleport.py
