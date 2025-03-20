```markdown
[NOTE] \*\*Embrace the power of DNS simulation and elevate your testing, security research, and learning experiences with this comprehensive tool. Happy testing and exploring!\*\*
```
# DNS Simulation Tool

A versatile and powerful DNS simulation tool designed to empower testing, development, and security research. This project creates a controlled environment that mimics real DNS behavior without relying on external servers. It’s perfect for developers, security researchers, and educators alike.

---

## Table of Contents

- [Overview](#overview)
- [What It’s Used For](#what-its-used-for)
    - [Testing and Development](#testing-and-development)
    - [Security Research](#security-research)
    - [Custom DNS Responses](#custom-dns-responses)
- [Advanced Techniques](#advanced-techniques)
    - [DNS Spoofing](#dns-spoofing)
    - [Traffic Analysis](#traffic-analysis)
    - [Load Testing](#load-testing)
    - [Custom DNS Filtering](#custom-dns-filtering)
    - [DNS Tunneling](#dns-tunneling)
    - [Educational Tool](#educational-tool)
- [How to Use](#how-to-use)
- [License](#license)

---## Overview

This project simulates a DNS server to provide a safe, isolated platform for:

- **Testing and debugging** DNS-based applications.
- **Analyzing network behavior** and DNS query patterns.
- **Customizing DNS responses** for specialized scenarios.
- **Educating users** about the inner workings of DNS protocols.

By using this tool, you can experiment and learn without impacting live systems, making it an essential asset for modern development and security practices.

---

## What It’s Used For

### Testing and Development

- **Simulated DNS Environment:**  
  Run the simulator to mimic a DNS server, allowing you to test DNS-related applications without dependency on a live server.

- **Debugging Made Easy:**  
  Use this tool to isolate and troubleshoot issues in your DNS-based tools, ensuring your applications work as intended.

### Security Research

- **Controlled Lab Setup:**  
  Create a sandbox environment to study how systems interact with DNS. This is ideal for monitoring query patterns and understanding DNS behavior.

- **Attack Simulation:**  
  Analyze DNS queries, detect anomalies, and even simulate DNS-based attacks (such as DNS spoofing) to test your defenses.

> **Example Use Case:**  
> Imagine you’re developing a web application that relies on DNS for service discovery. Use this simulator to generate consistent, controllable DNS responses in your test environment—ensuring your application behaves correctly without relying on external DNS servers.

### Custom DNS Responses

- **Dynamic Domain-IP Mapping:**  
  Customize how domain names are resolved by editing mappings between domains and IP addresses. This flexibility is useful for redirecting traffic or testing domain-specific configurations.

---

## Advanced Techniques

This tool can be extended for a variety of advanced use cases:

### DNS Spoofing

- **Simulated Malicious Redirects:**  
  Modify the simulator to return fraudulent IP addresses for targeted domains, allowing you to study the effects of DNS spoofing in a safe environment.

### Traffic Analysis

- **Enhanced Logging:**  
  Expand the logging functionality to capture and analyze DNS query patterns. Identify suspicious activity or monitor client behavior with detailed logs.

### Load Testing

- **Stress Simulation:**  
  Generate high volumes of DNS queries to evaluate the performance and resilience of your DNS servers or related systems under load.

### Custom DNS Filtering

- **Domain Blocking:**  
  Integrate logic to block or filter queries for certain domains—ideal for testing defenses against malware or unwanted content.

### DNS Tunneling

- **Covert Channel Experimentation:**  
  Use the simulator as part of a DNS tunneling setup to study data exfiltration techniques or establish secure, covert communication channels.

### Educational Tool

- **Learn DNS Internals:**  
  Perfect for educators and learners, the script demonstrates core DNS concepts, such as query parsing, response construction, and protocol handling.

---

## How to Use

### Running the Script

- **Basic Execution:**  
  Run the script with Python 3:
  ```bash
       python3 fake_dns.py
  ```
  - **Port Specific Basic Execution:**  
    Run the script with Python 3:
    ```bash
      python3 fake_dns.py 5353
    ```
  
```markdown
    - **Port Specific Execution with Custom Domain and IP:**  
        
        ** Run the script with Python 3:**
        ```bash
        python3 fake_dns.py 5353 example.com
        
   - [test case] -- testing the DNS server in different scenarios by sending various DNS queries in a safe environment.
        1. send legit dns query
        2. send spoofed dns query
        3. send invalid dns query
        4. send dns query with invalid domain
        5. send dns query with invalid ip
        6. send dns query with invalid port

## [Viewing Logs]
	•	Monitor DNS Activity:
        - Check the logs to see the DNS queries and responses.
        - The logs are stored in the same directory as the script.]
    •	[Log Files]:
    •	dns_queries.log --
        - Contains all DNS queries and responses.
    •	dns_queries_udp.log --
        - Contains DNS queries and responses over <UDP class="">
</UDP>
    •	dns_queries_tcp.log --
        - Contains DNS queries and responses over <TCP class="">
</TCP>

## [Detailed DNS query information is logged in]:
	•	dns_queries_udp.log
	•	dns_queries_tcp.log

## [Log Format]:
        - Each log entry includes:
            - Timestamp
            - Client IP address
            - Query type (A, AAAA, etc.)
            - Domain name
            - Response IP address
            - Response code (NOERROR, NXDOMAIN, etc.)
    •	[Log Rotation]:
        - The script rotates logs daily to prevent excessive file size.
        - Old logs are archived with a <timestamp class="">
        - Example: dns_queries_2023-10-01.log
        - The script uses the logging module to handle log rotation and archiving.
        - The log files are stored in the same directory as the script.

    - The logs include:
        - Timestamp
        - Client IP address
        - Query type (A, AAAA, etc.)
        - Domain name
        - Response IP address
        - Response code (NOERROR, NXDOMAIN, etc.)
    - The script uses the logging module to handle log rotation and archiving.
    - The log files are stored in the same directory as the script.
    - The script rotates logs daily to prevent excessive file size.
    - Old logs are archived with a timestamp.
    - Example: dns_queries_2023-10-01.log
```
```angular2html
  ## [Log Rotation] 
      - The script uses the logging module to handle log rotation and archiving.
      - The log files are stored in the same directory as the script.
      - The script rotates logs daily to prevent excessive file size.
      - Old logs are archived with a timestamp.
      - Example: <dns_queries_2023-10-01 class="log"> </dns_queries_2023-10-01>

# USE CASES 
## Custom Domain and IP
Modify the script to set custom domain-to-IP mappings. This allows you to simulate specific DNS responses for testing. The DNS response is constructed in the `handle` method of both the `DNSUDPHandler` and `DNSTCPHandler` classes. Here is a step-by-step explanation:

1. # **Parse the DNS request**:  
   The incoming DNS request is parsed using `DNSRecord.parse(data)` for UDP and `DNSRecord.parse(data[2:])` for TCP (skipping the first 2 bytes which are the length prefix in TCP DNS).

2. **Extract the query details**:  
   The queried domain name (`qname`) and query type (`qtype`) are extracted from the parsed request.

3. **Determine the IP address to return**:  
   The IP address to return in the response is determined by looking up the queried domain name in the `DOMAIN_IP_MAP` dictionary. If the domain is not found, a default IP address (`192.168.1.100`) is used.

4. **Log the query and response**:  
   The query details, including the client IP, queried domain, and response IP, are logged using the `log_query` function.

5. **Construct the DNS response**:  
   A DNS response is constructed using `DNSRecord`:
  - A new `DNSRecord` is created with the same header as the request and the original query.
  - An answer is added to the response using `reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))`, where `qname` is the queried domain, `QTYPE.A` indicates an A record, `rdata=A(ip_address)` sets the response IP address, and `ttl=60` sets the time-to-live for the response.

6. **Send the response**:
  - For UDP, the response is sent back to the client using `sock.sendto(reply.pack(), self.client_address)`.
  - For TCP, the response is sent back using `conn.sendall(len(response_data).to_bytes(2, 'big') + response_data)`.
  - The `conn.sendall` method sends the response data back to the client over TCP.
