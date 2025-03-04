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

## 🛠 Prerequisites  

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

🚀 Usage

Run the script with root privileges:

sudo ./tls_decryption.sh

You will be presented with an interactive menu offering the following options:

🔑 Generate CA Certificate for HTTPS Decryption
	•	Creates a CA certificate at ~/.bettercap-ca.cert.pem
	•	Verifies the certificate and displays details
	•	Copies the certificate to your current directory

🔍 Network Reconnaissance & Scanning
	•	Discover devices, MAC addresses, and IPs
	•	Perform OS fingerprinting and port scanning

📡 Monitor & Log Network Traffic
	•	View real-time traffic flows
	•	Save traffic data to a timestamped log file

🍪 Capture Cookies
	•	Extract session cookies from network traffic
	•	Save them for analysis

📊 Launch Web Dashboard
	•	Start Bettercap’s web interface
	•	View network activity graphically

⚙ How It Works

This script leverages Bettercap’s proxy capabilities to establish a MITM position. By creating a custom CA certificate and installing it on target devices, the script enables TLS/SSL decryption for traffic inspection.

📜 Certificate Distribution

After generating the CA certificate, you must install it on the target devices:
	•	📱 Android
	•	🍏 iOS
	•	💻 Windows
	•	🖥 macOS

🛠 Running Bettercap

Once the certificate is installed, start Bettercap with:

bettercap -eval "http.proxy on; https.proxy on; http.proxy.sslstrip true;"

⚠ Security & Ethical Considerations

This tool should only be used in environments where you have explicit authorization.
Legitimate use cases include:
✔ Network troubleshooting & debugging
✔ Security testing with permission
✔ Educational research
✔ Testing on your own personal devices

🚨 Legal Disclaimer

	Using this tool to intercept network traffic without authorization may violate privacy laws, computer fraud laws, and organizational policies. The author assumes no liability for misuse or any damages resulting from this tool. Use responsibly!

🛠 Troubleshooting

🔹 Certificate not generated?
➡ Run Bettercap manually and check for errors.

🔹 Certificate not trusted?
➡ Follow the correct installation steps for your OS.

🔹 No traffic intercepted?
➡ Verify network configuration and ensure traffic passes through the proxy.

📜 License

This project is licensed under the MIT License.

🚀 Start securing your network today! 🚀

---

### 📌 Improvements in This README:  
✅ **Clear structure & headings**  
✅ **Organized sections for easy navigation**  
✅ **Emojis for readability & engagement**  
✅ **Code blocks for commands**  
✅ **Legal disclaimer & security warnings**  

