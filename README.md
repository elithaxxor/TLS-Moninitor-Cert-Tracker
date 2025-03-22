# 🌐 TLS Monitor Cert Tracker and certSniff Integration

The **TLS Monitor Cert Tracker** program works with **certSniff** to monitor and track domain certificate events. Here is an overview of how they integrate:


## 🔒 TLS Monitor Cert Tracker

The main program is a utility script designed to set up **Bettercap** for TLS decryption through a **man-in-the-middle (MITM) proxy**. It automates the process of creating and deploying a Certificate Authority (CA) certificate used by Bettercap to intercept, decrypt, and inspect HTTPS traffic.

### Key Features:
- ✅ Bettercap installation check
- ✅ Automated CA certificate generation
- ✅ Certificate verification & easy distribution
- ✅ Network reconnaissance
- ✅ Traffic monitoring & logging
- ✅ Cookie capture from HTTP/HTTPS traffic
- ✅ Live network dashboard with a web interface

You can find more about this in the [README.md](./README.md).

## 🕵️ certSniff

**certSniff** is a Python-based keyword sniffer that uses the Certstream certificate transparency log data stream to monitor for domain certificate events containing specific keywords. It connects to a certificate transparency log stream and listens for new certificates. If the domains in these certificates contain specified keywords, it logs the matched domains.

![hacker2](https://github.com/user-attachments/assets/ecf8e56d-dd51-4cb5-806d-d5471958d39e)

### Features
- 🔍 Real-time Monitoring
- 📝 Keyword Matching
- 📁 Logging matched domains to a file (`log.txt`)
- 🗣️ Verbose Mode for detailed output
- 🌈 Colored Terminal Output for enhanced readability

Installation and usage instructions can be found in the [certSniff README.md](./certSniff/README.md).

## 🔗 Integration

The integration between the **TLS Monitor Cert Tracker** and **certSniff** involves:

- **Monitoring Certificate Events**: certSniff monitors real-time certificate transparency logs for domain certificates containing specified keywords.
- **Logging and Alerting**: When a keyword match is found, certSniff logs the details, which can be utilized by the TLS Monitor Cert Tracker for further analysis or alerting.

The integration allows for comprehensive monitoring and logging of certificate events, enhancing the capabilities of the TLS decryption and monitoring setup provided by the main program.

For more detailed instructions on setting up and running certSniff, refer to the [certSniff documentation](./certSniff/README.md).
