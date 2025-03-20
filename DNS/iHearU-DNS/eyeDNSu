#!/usr/bin/env python3
"""
fake_dns.py
This script implements a fake DNS server that returns different IP addresses based on the queried domain.
It logs client IP addresses, DNS queries, and their frequency to separate files for UDP and TCP.
It supports both UDP and optional TCP.
"""

import socketserver
import sys
import logging
from collections import defaultdict
from dnslib import DNSRecord, QTYPE, RR, A

# Configure logging for UDP and TCP separately
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(client_ip)s - %(query)s - %(response)s - %(frequency)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
udp_logger = logging.getLogger("udp_logger")
tcp_logger = logging.getLogger("tcp_logger")
udp_handler = logging.FileHandler("dns_queries_udp.log")
tcp_handler = logging.FileHandler("dns_queries_tcp.log")
udp_logger.addHandler(udp_handler)
tcp_logger.addHandler(tcp_handler)

# Dictionary to track query frequency
udp_query_tracker = defaultdict(int)
tcp_query_tracker = defaultdict(int)

def log_query(logger, query_tracker, client_ip, query, response):
    query_tracker[(client_ip, query)] += 1
    logger.info("Query received", extra={
        "client_ip": client_ip,
        "query": query,
        "response": response,
        "frequency": query_tracker[(client_ip, query)]
    })

# Dictionary mapping domain names to IP addresses.
DOMAIN_IP_MAP = {
    "example.com.": "192.168.1.101",
    "test.com.": "192.168.1.102",
    # Add more domain-IP mappings as needed.
}

class DNSUDPHandler(socketserver.BaseRequestHandler):
    """
    DNSHandler class to handle incoming DNS requests over UDP.
    It parses the request, logs the query, and constructs a response with the corresponding IP address.
    """
    def handle(self):
        data, sock = self.request
        client_ip = self.client_address[0]  # Extract client IP
        try:
            request = DNSRecord.parse(data)
        except Exception as e:
            udp_logger.error(f"Failed to parse DNS request from {client_ip}: {e}")
            return
        
        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        
        # Determine the IP address to return based on the queried domain.
        ip_address = DOMAIN_IP_MAP.get(qname, "192.168.1.100")  # Default IP if domain not found.
        
        # Log the query and response
        log_query(udp_logger, udp_query_tracker, client_ip, qname, ip_address)
        query_count = udp_query_tracker[(client_ip, qname)]
        print(f"Received UDP query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Query count: {query_count})")
        
        # Build a DNS response with an A record using the determined IP.
        reply = DNSRecord(DNSRecord.header(request), q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        sock.sendto(reply.pack(), self.client_address)

class DNSTCPHandler(socketserver.BaseRequestHandler):
    """
    DNSHandler class to handle incoming DNS requests over TCP.
    """
    def handle(self):
        conn = self.request
        client_ip = self.client_address[0]
        try:
            data = conn.recv(1024)
            request = DNSRecord.parse(data[2:])  # Skip first 2 bytes (length prefix in TCP DNS)
        except Exception as e:
            tcp_logger.error(f"Failed to parse DNS request from {client_ip} over TCP: {e}")
            return
        
        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        
        ip_address = DOMAIN_IP_MAP.get(qname, "192.168.1.100")
        log_query(tcp_logger, tcp_query_tracker, client_ip, qname, ip_address)
        query_count = tcp_query_tracker[(client_ip, qname)]
        print(f"Received TCP query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Query count: {query_count})")
        
        reply = DNSRecord(DNSRecord.header(request), q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        response_data = reply.pack()
        conn.sendall(len(response_data).to_bytes(2, 'big') + response_data)
        conn.close()

if __name__ == "__main__":
    # Allow port override via command-line argument.
    port = 53
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    print(f"Starting fake DNS server on UDP and TCP port {port}")
    udp_server = socketserver.UDPServer(('', port), DNSUDPHandler)
    tcp_server = socketserver.TCPServer(('', port), DNSTCPHandler)
    
    try:
        from threading import Thread
        udp_thread = Thread(target=udp_server.serve_forever)
        tcp_thread = Thread(target=tcp_server.serve_forever)
        
        udp_thread.start()
        tcp_thread.start()
        
        udp_thread.join()
        tcp_thread.join()
    except KeyboardInterrupt:
        print("Shutting down fake DNS server.")

