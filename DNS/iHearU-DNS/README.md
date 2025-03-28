```markdown

<img width="422" alt="Screenshot 2025-03-21 at 10 15 37 PM" src="https://github.com/user-attachments/assets/070bee21-7ff3-4349-ba70-45c68687b09d" />


## [Overiew]

### -->  I recommend running eyeDNSasync_III in debug mode. otherwise it will run silent.

--> It uses asynchronous I/O (via asyncio) for UDP and TCP servers, supports multiple record types (A, AAAA, MX, etc.) from a dynamic JSON config, caches responses with TTL, and includes enhanced security and logging. We also add an interactive menu that lets the operator choose whether to log queries, reroute them to a fixed IP, or do both.

The file `eyeDNSu` is a Python script that implements a fake DNS server. Here is a detailed explanation of its functionality:

--> Responds to DNS requests over both UDP and TCP
--> Asynchronous Handling / or Threaded. Two distinct files are posted. 
--> Simultaneously manages multiple DNS requests without blocking or Custom Logging
--> Logs client IPs, queried domains, responses, and frequencies
--> Verbose Output
--> Clear colored console output for easy debugging and monitoring
--> Log File Management
--> Deletes logs automatically once reaching 5 GB size


🎯 Why is Async Better Here? (Bottom Line)
	•	DNS serving is an I/O-bound operation—network I/O dominates the workload.
	•	Async (asyncio) excels precisely at I/O-bound workloads, managing thousands of connections with minimal overhead.
	•	Low overhead and high scalability are crucial for DNS servers, making asyncio preferable over multi-threading or multi-processing.
```
![Memory Overhead](https://github.com/user-attachments/assets/a4582ed7-0d14-44e6-bb79-16832fe31252)

```markdown
## Logging Configuration:
- The script sets up logging for both UDP and TCP DNS queries. It logs client IP addresses, the DNS queries made, the responses sent, and the frequency of each query.

## Query Tracking:
- The script uses dictionaries to keep track of how many times each client IP has queried each domain.

## Domain-IP Mapping:
- A dictionary (`DOMAIN_IP_MAP`) maps domain names to specific IP addresses. If a queried domain is not found in the dictionary, a default IP address (`192.168.1.100`) is returned.

## DNS Query Handling:
- The script defines two handler classes (`DNSUDPHandler` and `DNSTCPHandler`) to handle DNS queries over UDP and TCP, respectively.
- Each handler parses the DNS query, logs the query details, determines the appropriate IP address to return, and sends back a DNS response with an A record containing that IP address.

## Server Setup:
- In the main block, the script sets up UDP and TCP servers on port 53 (or a custom port if provided via command-line argument).
- It starts the servers and handles incoming DNS queries using separate threads for UDP and TCP.

## Graceful Shutdown:
- The script can be terminated using a keyboard interrupt, which will shut down the servers gracefully.

## Example of Usage:

To run the script, you would use a command like `python3 eyeDNSu` or `python3 eyeDNSu <custom_port>`.
The script will then start listening for DNS queries on the specified port and respond according to the domain-IP mappings defined in the `DOMAIN_IP_MAP` dictionary.

For more detailed information, you can view the file on GitHub.
```



iDNS_CUP
=====================================
Overview


# Explanation of the `eyeDNSu` File

The file `eyeDNSu` is a Python script that implements a fake DNS server. Here is a detailed explanation of its functionality:

## Logging Configuration:
- The script sets up logging for both UDP and TCP DNS queries. It logs client IP addresses, the DNS queries made, the responses sent, and the frequency of each query.

## Query Tracking:
- The script uses dictionaries to keep track of how many times each client IP has queried each domain.

## Domain-IP Mapping:
- A dictionary (`DOMAIN_IP_MAP`) maps domain names to specific IP addresses. If a queried domain is not found in the dictionary, a default IP address (`192.168.1.100`) is returned.

## DNS Query Handling:
- The script defines two handler classes (`DNSUDPHandler` and `DNSTCPHandler`) to handle DNS queries over UDP and TCP, respectively.
- Each handler parses the DNS query, logs the query details, determines the appropriate IP address to return, and sends back a DNS response with an A record containing that IP address.

## Server Setup:
- In the main block, the script sets up UDP and TCP servers on port 53 (or a custom port if provided via command-line argument).
- It starts the servers and handles incoming DNS queries using separate threads for UDP and TCP.

## Graceful Shutdown:
- The script can be terminated using a keyboard interrupt, which will shut down the servers gracefully.

## Example of Usage:

To run the script, you would use a command like `python3 eyeDNSu` or `python3 eyeDNSu <custom_port>`.
The script will then start listening for DNS queries on the specified port and respond according to the domain-IP mappings defined in the `DOMAIN_IP_MAP` dictionary.

For more detailed information, you can view the file on GitHub.




Use Cases
The iDNS_CUP script is designed for various purposes, including:

    Testing and Development: Simulate a DNS server for testing applications that rely on DNS resolution and debug DNS-related issues in a controlled environment.
    DNS Spoofing or Redirection: Redirect DNS queries to specific IP addresses for testing how applications behave when DNS responses are manipulated or simulating malicious DNS spoofing attacks.
    Logging and Monitoring: Monitor DNS traffic and analyze query patterns by logging all DNS queries.
    Educational Purposes: Serve as a practical example of how DNS servers work and how to implement one using Python.

Functionality
DNS Query Handling
The script implements a fake DNS server that listens for DNS queries over both UDP and TCP. Key features include:

    Listening for DNS queries on port 53 (default DNS port) or a custom port specified via a command-line argument.
    Parsing incoming DNS queries using the dnslib library.
    Mapping the queried domain name to a predefined IP address using the DOMAIN_IP_MAP dictionary, with a default IP address (192.168.1.100) if the domain is not found.

Logging
The script logs details of each DNS query, including:

    Client IP address
    Queried domain name
    Response IP address
    Frequency of the query (how many times the same client has queried the same domain)
    Separate log files are maintained for UDP and TCP queries (dns_queries_udp.log and dns_queries_tcp.log).

UDP and TCP Support
The server handles DNS queries over both UDP and TCP protocols, with:

    TCP handling the DNS length prefix (the first two bytes) as required by the DNS-over-TCP protocol.

Query Frequency Tracking
The script tracks how often each client queries each domain using two dictionaries (udp_query_tracker and tcp_query_tracker).
Threading
The server runs two threads to spawn one UDP and one TCP daemon, simultaneously handling both protocols.
Getting Started
To use this script, run it with Python, specifying a custom port if desired. The script will start listening to DNS queries and logging them into the specified log files.
Technical Details
Protocol Layers

    UDP: Operates at the OSI model's Transport Layer (Layer 4).
    TCP: Also operates at Layer 4, but with additional reliability features.
    DNS: An Application Layer (Layer 7) protocol.
    The script leverages multi-threading (2 cores, 2 layers) to ensure compatibility with larger DNS responses.

Layer Breakdown

    Layer 4 (Transport Layer): UDP and TCP protocols.
    Layer 7 (Application Layer): DNS protocol.
    The script implements both DNSUDPHandler and DNSTCPHandler to handle DNS queries over UDP and TCP, respectively.
