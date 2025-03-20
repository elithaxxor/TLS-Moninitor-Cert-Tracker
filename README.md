# TLS Decryption Script

A utility script for setting up **Bettercap** to perform TLS decryption through a **man-in-the-middle (MITM) proxy**.

## 📖 Overview
This script automates the process of **creating and deploying a Certificate Authority (CA) certificate** used by Bettercap to **intercept, decrypt, and inspect HTTPS traffic**.

It is designed for:
- **Network security professionals**
- **Penetration testers**
- **System administrators**

⚠ **Use this tool responsibly and only in environments where you have explicit permission.**

## ✨ Features

✅ **Bettercap installation check**
✅ **Automated CA certificate generation**
✅ **Certificate verification & easy distribution**
✅ **Guidance for certificate installation (Windows, macOS, Android, iOS)**
✅ **Network reconnaissance** (discover & scan devices)
✅ **Traffic monitoring & logging**
✅ **Cookie capture from HTTP/HTTPS traffic**
✅ **Live network dashboard with a web interface**

---

### 🔍 **Network Reconnaissance**
- Discover devices on the local network
- Identify device type, hostname, and IP address
- Perform OS fingerprinting and port scanning

### 📡 **Traffic Monitoring & Logging**
- View real-time traffic flows
- Analyze source & destination IP addresses
- Log **DNS requests, MAC addresses, and IPs**

### 🍪 **Capture Cookies**
- Extract cookies from HTTP/HTTPS traffic
- Save session data for further analysis

### 📊 **Web Dashboard**
- Launch Bettercap's web interface
- Graphical network activity overview
- Access at [`http://127.0.0.1:80`](http://127.0.0.1:80)

---

## 🛠️ Prerequisites

- Linux-based OS
- **Bettercap** installed
- **OpenSSL** installed
- Root / sudo privileges
- **Nmap** (optional, for enhanced device fingerprinting)

## 📥 Installation

Clone this repository and make the script executable:

```bash
git clone https://github.com/your-repo/tls-decryption-script.git
cd tls-decryption-script
chmod +x tls_decryption.sh
