#!/usr/bin/env python3
"""
fake_dns.py
This script implements a fake DNS server that returns different IP addresses based on the queried domain.
It logs client IP addresses, DNS queries, and their frequency to a file.
It supports both UDP and optional TCP.
"""

import socketserver
import sys
import logging
from logging.handlers import RotatingFileHandler
from collections import defaultdict
from dnslib import DNSRecord, QTYPE, RR, A

# Configure logging with rotation
log_handler = RotatingFileHandler("dns_queries.log", maxBytes=5*1024*1024, backupCount=5)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger = logging.getLogger("DNSLogger")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

logging.basicConfig(
    filename="dns_queries.log",
    level=logging.INFO,
    format="%(asctime)s - %(client_ip)s - %(query)s - %(response)s - %(frequency)s - %(query_type)s - %(response_code)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Dictionary to track query frequency
query_tracker = defaultdict(int)

def log_query(client_ip, query, response):
    """
    Logs the DNS query details including client IP, query, response, and frequency.

    Args:
        client_ip (str): The IP address of the client making the query.
        query (str): The domain name being queried.
        response (str): The IP address returned in response to the query.
    """
    query_tracker[(client_ip, query)] += 1
    frequency = query_tracker[(client_ip, query)]
    logger.info(f"Client: {client_ip}, Query: {query}, Response: {response}, Frequency: {frequency}")

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
        """
        Handles incoming DNS requests over UDP.
        """
        data, sock = self.request
        client_ip = self.client_address[0]
        # Log the client IP address
        logger.info(f"Received DNS request from {client_ip}")
        print(f"Received DNS request from {client_ip}")
        # Increment the query count for the client IP
        query_tracker[client_ip] += 1
        try:
            request = DNSRecord.parse(data)
            print(f"[!]Parsed UDP DNS request: {request}")
            logger.info(f"Parsed UDP DNS request: {request}")

        except Exception as e:
            logger.error(f"Failed to parse DNS request from {client_ip}: {e}")
            print(f"Failed to parse DNS request from {client_ip}: {e}")
            return

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        ip_address = DOMAIN_IP_MAP.get(qname, "192.168.1.100")

        log_query(client_ip, qname, ip_address)
        query_count = query_tracker[(client_ip, qname)]
        print(f"Received query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Query count: {query_count})")

        reply = DNSRecord(DNSRecord.header(request), q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        sock.sendto(reply.pack(), self.client_address)

class DNSTCPHandler(socketserver.BaseRequestHandler):
    """
    DNSHandler class to handle incoming DNS requests over TCP.
    """
    def handle(self):
        """
        Handles incoming DNS requests over TCP.
        """
        conn = self.request
        client_ip = self.client_address[0]
        try:
            data = conn.recv(1024)
            request = DNSRecord.parse(data[2:])
        except Exception as e:
            logger.error(f"Failed to parse DNS request from {client_ip} over TCP: {e}")
            conn.close()
            return

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        ip_address = DOMAIN_IP_MAP.get(qname, "192.168.1.100")

        log_query(client_ip, qname, ip_address)
        query_count = query_tracker[(client_ip, qname)]
        print(f"Received TCP query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Query count: {query_count})")

        reply = DNSRecord(DNSRecord.header(request), q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        response_data = reply.pack()
        conn.sendall(len(response_data).to_bytes(2, 'big') + response_data)
        conn.close()

    def finish(self):
        """
        Finish the request handling.
        """
        self.request.close()
        print(f"Connection closed for {self.client_address[0]}")


def shutdown_server(server):
    """
    Shuts down the server gracefully.
    Args:
        server: The server instance to shut down.
    """
    server.shutdown()
    server.server_close()
    print("Server shut down gracefully.")
    logger.info("Server shut down gracefully.")

    # Optionally, you can also log the shutdown event
    logging.info("Server shut down gracefully.")
def main():
    """
    Main function to start the fake DNS server on UDP and TCP ports.
    """
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

    except Exception as e:
        logger.error(f"[-] Error starting server: {e}")
        print(f"[-] Error starting server: {e}")
        udp_server.shutdown()
        tcp_server.shutdown()
        print("[-] Fake DNS server shut down.")

    except KeyboardInterrupt:
        print("[-] Keyboard shutdown.. Shutting down fake DNS server.")
        logger.error("[-] Keyboard shutdown.. Shutting down fake DNS server.")
        udp_server.shutdown()
        tcp_server.shutdown()
        print("[-] Fake DNS server shut down.")
        logger.info("[-] Fake DNS server shut down.")

if __name__ == "__main__":
    port = 53
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    main()