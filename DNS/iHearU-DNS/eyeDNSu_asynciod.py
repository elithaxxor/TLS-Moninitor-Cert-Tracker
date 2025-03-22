#!/usr/bin/env python3


import asyncio
import sys
import logging
import os
from collections import defaultdict
from dnslib import DNSRecord, QTYPE, RR, A
from logging.handlers import RotatingFileHandler

# --- Verbose Output Helper ---
def verbose_print(message, level="good"):
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    if level == "good":
        prefix = f"{GREEN}[+]{RESET}"
    elif level == "bad":
        prefix = f"{RED}[-]{RESET}"
    elif level == "system":
        prefix = f"{RED}[!]{RESET}"
    else:
        prefix = ""
    print(f"{prefix} {message}")

# --- Custom Log Handler ---
class DeletingRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        try:
            os.remove(self.baseFilename)
        except OSError:
            pass
        # Reopen stream for new log file.
        self.stream = self._open()

# 5GB in bytes.
MAX_LOG_SIZE = 5 * 1024 * 1024 * 1024

# --- Logger Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(client_ip)s - %(query)s - %(response)s - %(frequency)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
udp_logger = logging.getLogger("udp_logger")
tcp_logger = logging.getLogger("tcp_logger")
udp_handler = DeletingRotatingFileHandler("dns_queries_udp.log", maxBytes=MAX_LOG_SIZE, backupCount=0)
tcp_handler = DeletingRotatingFileHandler("dns_queries_tcp.log", maxBytes=MAX_LOG_SIZE, backupCount=0)
udp_logger.addHandler(udp_handler)
tcp_logger.addHandler(tcp_handler)

# --- Query Tracker Dictionaries ---
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

# --- Domain to IP Mapping ---
DOMAIN_IP_MAP = {
    "example.com.": "192.168.1.101",
    "test.com.": "192.168.1.102",
    # Add more domain-IP mappings as needed.
}

# --- Asynchronous UDP Server Implementation ---
class DNSUDPProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        verbose_print("UDP server started", level="system")

    def datagram_received(self, data, addr):
        client_ip = addr[0]
        try:
            request = DNSRecord.parse(data)
        except Exception as e:
            udp_logger.error(f"Failed to parse DNS request from {client_ip}: {e}")
            verbose_print(f"Failed to parse UDP DNS request from {client_ip}: {e}", level="bad")
            return
        
        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        
        # Determine the IP address to return based on the queried domain.
        ip_address = DOMAIN_IP_MAP.get(qname, "192.168.1.100")  # Default IP if domain not found.
        
        # Log the query and response.
        log_query(udp_logger, udp_query_tracker, client_ip, qname, ip_address)
        query_count = udp_query_tracker[(client_ip, qname)]
        verbose_print(f"Received UDP query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Query count: {query_count})", level="good")
        
        # Build DNS response with an A record using the determined IP.
        reply = DNSRecord(DNSRecord.header(request), q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        self.transport.sendto(reply.pack(), addr)

# --- Asynchronous TCP Handler ---
async def handle_tcp_client(reader, writer):
    peername = writer.get_extra_info('peername')
    client_ip = peername[0] if peername else "Unknown"
    try:
        # Read the first 2 bytes to get the length of the DNS message.
        length_bytes = await reader.readexactly(2)
        msg_length = int.from_bytes(length_bytes, 'big')
        data = await reader.readexactly(msg_length)
        request = DNSRecord.parse(data)
    except Exception as e:
        tcp_logger.error(f"Failed to parse DNS request from {client_ip} over TCP: {e}")
        verbose_print(f"Failed to parse TCP DNS request from {client_ip}: {e}", level="bad")
        writer.close()
        await writer.wait_closed()
        return
    
    qname = str(request.q.qname)
    qtype = QTYPE[request.q.qtype]
    ip_address = DOMAIN_IP_MAP.get(qname, "192.168.1.100")
    
    log_query(tcp_logger, tcp_query_tracker, client_ip, qname, ip_address)
    query_count = tcp_query_tracker[(client_ip, qname)]
    verbose_print(f"Received TCP query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Query count: {query_count})", level="good")
    
    reply = DNSRecord(DNSRecord.header(request), q=request.q)
    reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
    response_data = reply.pack()
    response_length = len(response_data).to_bytes(2, 'big')
    writer.write(response_length + response_data)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

# --- Main Async Function ---
async def main():
    # Allow port override via command-line argument.
    port = 53
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    verbose_print(f"Starting asynchronous fake DNS server on UDP and TCP port {port}", level="system")
    loop = asyncio.get_running_loop()

    # Start UDP server.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: DNSUDPProtocol(),
        local_addr=('0.0.0.0', port)
    )
    
    # Start TCP server.
    tcp_server = await asyncio.start_server(handle_tcp_client, '0.0.0.0', port)
    
    async with tcp_server:
        try:
            await asyncio.gather(
                tcp_server.serve_forever(),
                asyncio.sleep(float('inf'))  # Keeps the UDP server running.
            )
        except asyncio.CancelledError:
            pass
        finally:
            transport.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        verbose_print("Shutting down asynchronous fake DNS server.", level="system")
