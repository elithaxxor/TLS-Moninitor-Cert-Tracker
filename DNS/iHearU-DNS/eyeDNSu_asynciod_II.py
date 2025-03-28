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
import threading
import socket
import unittest
import time
import json
import fnmatch
from collections import defaultdict
from dnslib import DNSRecord, QTYPE, RR, A

# Configure base logging format for handlers
LOG_FORMAT = "%(asctime)s - %(client_ip)s - %(query)s - %(response)s - %(frequency)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Initialize loggers for UDP and TCP
udp_logger = logging.getLogger("udp_logger")
tcp_logger = logging.getLogger("tcp_logger")

udp_handler = logging.FileHandler("dns_queries_udp.log")
tcp_handler = logging.FileHandler("dns_queries_tcp.log")

formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
udp_handler.setFormatter(formatter)
tcp_handler.setFormatter(formatter)

udp_logger.setLevel(logging.INFO)
tcp_logger.setLevel(logging.INFO)

udp_logger.addHandler(udp_handler)
tcp_logger.addHandler(tcp_handler)

# Track query frequencies
udp_query_tracker = defaultdict(int)
tcp_query_tracker = defaultdict(int)

def log_query(logger, query_tracker, client_ip, query, response):
    query_tracker[(client_ip, query)] += 1
    log_data = {
        "client_ip": client_ip,
        "query": query,
        "response": response,
        "frequency": query_tracker[(client_ip, query)]
    }
    logger.info("Query received", extra=log_data)

def add_stdout_logging():
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    udp_logger.addHandler(stdout_handler)
    tcp_logger.addHandler(stdout_handler)

# Load domain to IP mapping from config file
CONFIG_PATH = "dns_config.json"
def load_domain_ip_map():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load config file '{CONFIG_PATH}': {e}")
        return {}

DOMAIN_IP_MAP = load_domain_ip_map()
DEFAULT_IP = "192.168.1.100"

def resolve_ip(qname):
    if qname in DOMAIN_IP_MAP:
        return DOMAIN_IP_MAP[qname]
    for pattern, ip in DOMAIN_IP_MAP.items():
        if '*' in pattern and fnmatch.fnmatch(qname, pattern):
            return ip
    return DEFAULT_IP

class DNSUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        client_ip = self.client_address[0]
        try:
            request = DNSRecord.parse(data)
        except Exception as e:
            udp_logger.error(f"Failed to parse DNS request from {client_ip}: {e}")
            return

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        if qtype != "A":
            print(f"Unsupported query type {qtype} from {client_ip} for {qname}")
            return

        ip_address = resolve_ip(qname)
        log_query(udp_logger, udp_query_tracker, client_ip, qname, ip_address)
        count = udp_query_tracker[(client_ip, qname)]
        print(f"Received UDP query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Count: {count})")

        reply = DNSRecord(header=request.header, q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        sock.sendto(reply.pack(), self.client_address)

class DNSTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        client_ip = self.client_address[0]
        try:
            data = conn.recv(1024)
            request = DNSRecord.parse(data[2:])
        except Exception as e:
            tcp_logger.error(f"Failed to parse DNS request from {client_ip} over TCP: {e}")
            return

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        if qtype != "A":
            print(f"Unsupported query type {qtype} from {client_ip} for {qname}")
            return

        ip_address = resolve_ip(qname)
        log_query(tcp_logger, tcp_query_tracker, client_ip, qname, ip_address)
        count = tcp_query_tracker[(client_ip, qname)]
        print(f"Received TCP query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Count: {count})")

        reply = DNSRecord(header=request.header, q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        response_data = reply.pack()
        conn.sendall(len(response_data).to_bytes(2, 'big') + response_data)
        conn.close()

def start_dns_servers(port=5353):
    udp_server = socketserver.UDPServer(("", port), DNSUDPHandler)
    tcp_server = socketserver.TCPServer(("", port), DNSTCPHandler)
    udp_thread = threading.Thread(target=udp_server.serve_forever, daemon=True)
    tcp_thread = threading.Thread(target=tcp_server.serve_forever, daemon=True)
    udp_thread.start()
    tcp_thread.start()
    return udp_server, tcp_server

class TestFakeDNSServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 5353
        cls.udp_server, cls.tcp_server = start_dns_servers(cls.port)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.udp_server.shutdown()
        cls.tcp_server.shutdown()

    def test_udp_dns_query(self):
        qname = "example.com."
        request = DNSRecord.question(qname)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(request.pack(), ("127.0.0.1", self.port))
        data, _ = sock.recvfrom(1024)
        response = DNSRecord.parse(data)
        self.assertEqual(str(response.q.qname), qname)
        self.assertEqual(str(response.rr[0].rdata), DOMAIN_IP_MAP[qname])

    def test_tcp_dns_query(self):
        qname = "test.com."
        request = DNSRecord.question(qname)
        data = request.pack()
        prefixed_data = len(data).to_bytes(2, 'big') + data
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect(("127.0.0.1", self.port))
        sock.sendall(prefixed_data)
        resp_len = int.from_bytes(sock.recv(2), 'big')
        response = DNSRecord.parse(sock.recv(resp_len))
        self.assertEqual(str(response.q.qname), qname)
        self.assertEqual(str(response.rr[0].rdata), DOMAIN_IP_MAP[qname])

    def test_unsupported_query_type(self):
        qname = "example.com."
        request = DNSRecord.question(qname, qtype="MX")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(request.pack(), ("127.0.0.1", self.port))
        try:
            data, _ = sock.recvfrom(1024)
            response = DNSRecord.parse(data)
            self.assertFalse(response.rr)  # Should not return any answers
        except socket.timeout:
            self.assertTrue(True)

if __name__ == "__main__":
    debug_mode = '--debug' in sys.argv
    if debug_mode:
        add_stdout_logging()
    if 'test' in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        port = 53
        for arg in sys.argv[1:]:
            if arg.isdigit():
                port = int(arg)
        print(f"Starting fake DNS server on UDP and TCP port {port}")
        DOMAIN_IP_MAP = load_domain_ip_map()
        udp_server = socketserver.UDPServer(('', port), DNSUDPHandler)
        tcp_server = socketserver.TCPServer(('', port), DNSTCPHandler)
        try:
            udp_thread = threading.Thread(target=udp_server.serve_forever)
            tcp_thread = threading.Thread(target=tcp_server.serve_forever)
            udp_thread.start()
            tcp_thread.start()
            udp_thread.join()
            tcp_thread.join()
        except KeyboardInterrupt:
            print("Shutting down fake DNS server.")
