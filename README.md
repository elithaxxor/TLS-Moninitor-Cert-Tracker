
```markdown
# TLS Decryption Script

A utility script for setting up Bettercap to perform TLS decryption through a man-in-the-middle proxy.

## Overview

This script automates the process of creating and deploying a Certificate Authority (CA) certificate used by Bettercap to intercept, decrypt, and inspect HTTPS traffic. It's designed for network security professionals, penetration testers, and system administrators.

## Purpose
The script is essentially creating a monitoring station on your computer. All the reconnaissance, scanning, and traffic analysis happens from your machine, analyzing the traffic it can see on the network. For ethical testing, this should be done only in environments where you have permission to monitor the network, such as your personal network, a lab environment, or a client network with proper authorization.
![Uploading logo2.png…]()


![logo2](https://github.com/user-attachments/assets/0490f291-8ac4-4995-ab6d-0430445460f3)

Run on your computer - You'll need:
- Linux-based system (works best on Kali, Ubuntu, Debian, etc.)
- Bettercap installed
- Root/sudo privileges
- A network interface that can see the target traffic

Network positioning - Your computer needs to be positioned in one of these ways:
1. On the same network as the targets
2. As a gateway/router that traffic passes through
3. In a position to perform ARP spoofing (which Bettercap can help with)

Certificate distribution - After generating the CA certificate on your computer:
- You'll need to distribute and install this certificate on any target devices
- Only then can you decrypt their HTTPS traffic.

## Features
- Checks for Bettercap installation
- Generates a CA certificate automatically
- Verifies successful certificate creation
- Copies the certificate for easy distribution
- Provides guidance for certificate installation on various operating systems
- Network reconnaissance to discover devices
  - Computer/device type identification
  - Hostname resolution
  - IP address mapping
- Detailed device scanning with OS fingerprinting
- Traffic monitoring to analyze network destinations
- Live network dashboard with web interface

## Prerequisites
- Linux-based operating system
- Bettercap installed
- OpenSSL installed
- Root or sudo privileges
- Nmap (optional, for enhanced device fingerprinting)

## Installation
1. Clone or download this script to your local machine
2. Make the script executable:
   ```bash
   chmod +x tls_decryption.sh
   ```

## Usage
Run the script with root privileges:
```bash
sudo ./tls_decryption.sh
```

The script will present an interactive menu with the following options:
1. **Generate CA certificate for HTTPS decryption**
   - Creates a certificate at `~/.bettercap-ca.cert.pem`
   - Verifies the certificate and displays its details
   - Copies the certificate to your current directory

2. **Network reconnaissance**
   - Discovers devices on the local network
   - Shows MAC addresses, IP addresses, and hostnames when available
   - Displays vendor information to help identify device types

3. **Detailed device scan**
   - Performs OS fingerprinting to determine device types
   - Scans for open ports and services
   - Provides more comprehensive device identification

4. **Monitor network traffic**
   - Shows real-time traffic flows
   - Displays source and destination IP addresses
   - Identifies protocols and services being used

5. **Launch web dashboard**
   - Starts Bettercap's web interface
   - Provides a graphical view of network activity
   - Accessible via browser at [http://127.0.0.1:80](http://127.0.0.1:80)

## How It Works
The script leverages Bettercap's proxy capabilities to set up a man-in-the-middle position. By creating a custom CA certificate and installing it on target devices, the script enables the decryption of HTTPS traffic.

### Certificate Distribution
After generating the certificate, you must distribute and install it on any device you wish to monitor. The script provides guidance for installing the certificate on:
- Android
- iOS
- Windows
- macOS

### Running Bettercap
Once the certificate is installed on target devices, you can run Bettercap with the following command to begin intercepting traffic:
```bash
bettercap -eval "http.proxy on; https.proxy on; http.proxy.sslstrip true;"
```

## Security and Ethical Considerations
This tool should only be used in environments where you have explicit permission to monitor network traffic. Potential legitimate uses include:
- Network troubleshooting and debugging
- Security testing with proper authorization
- Educational environments
- Your own personal devices

## Troubleshooting
- **Certificate not generated**: Run Bettercap manually and check for errors
- **Certificate not trusted**: Ensure you've followed the correct installation steps for the target OS
- **No traffic intercepted**: Verify network configuration and routing to ensure traffic passes through the proxy

## Legal Disclaimer
Using this tool to intercept network traffic without authorization may violate computer fraud and abuse laws, privacy laws, and organizational policies. The author of this script assumes no liability for unauthorized use.

## License
This script is provided "as is" without warranty of any kind. You are free to modify and distribute it according to your needs.
```

You can view the original file [here](https://github.com/elithaxxor/TLS-Moninitor-Cert-Tracker/blob/main_pi/README2.md).
