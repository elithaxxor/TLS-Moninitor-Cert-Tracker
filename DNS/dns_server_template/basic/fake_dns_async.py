import socketserver, socket, asyncio, logging, sys
from dnslib import DNSRecord, QTYPE, RR, A
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from collections import defaultdict
from dnslib import DNSRecord, QTYPE, RR, A, DNSHeader, DNSQuestion
from logging.handlers import RotatingFileHandler

# Configure logging#################################################
# Dictionary mapping domain names to IP addresses.
DOMAIN_IP_MAP = {
    "example.com.": "192.168.1.101",
    "test.com.": "192.168.1.102",
    # Add more domain-IP mappings as needed.
}
####################################################################

# Configure logging with rotation-- this will create a new log file when the current one reaches 10MB
log_handler = RotatingFileHandler("dns_queries.log", maxBytes=10*1024*1024, backupCount=5)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger = logging.getLogger("DNSLogger")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

port = 53  # DNS port
query_tracker = {}
def log_query(client_ip, query, response):
    query_tracker[(client_ip, query)] += 1
    frequency = query_tracker[(client_ip, query)]
    print(f"Client: {client_ip}, Query: {query}, Response: {response}, Frequency: {frequency}")
# Dictionary to track query frequency

# query_tracker = default dict(int)  # Track query frequency

class DNSUDPHandler(socketserver.BaseRequestHandler):
    """
    DNSHandler class to handle incoming DNS requests over UDP.
    It parses the request, logs the query, and constructs a response with the corresponding IP address.
    """
    def handle(self):
        data, sock = self.request
        client_ip = self.client_address[0]
        # Log the client IP address
        logger.info(f"Received DNS request from {client_ip}")
        print(f"Received DNS request from {client_ip}")
        # Increment the query count for the client IP
        query_tracker[client_ip] += 1
        try:
            request = DNSRecord.parse(data)
            print(f"[!]Parsed UDP DNS request: {client_ip} : {request}")
            logger.info(f"Parsed UDP DNS request: {client_ip} : {request}")

        except Exception as e:
            logger.error(f"Failed to parse DNS request from {client_ip}: {e}")
            print(f"Failed to parse DNS request from {client_ip}: {e}")
            return

        qname = str(request.q.qname)
        # qtype = QTYPE[request.q.qtype]
        # IP address mapping
        # ip_address = DOMAIN_IP_MAP.get(qname, "
        qtype = QTYPE[request.q.qtype]
        ip_address = DOMAIN_IP_MAP.get(qname, "192.168.1.100")

        log_query(client_ip, qname, ip_address)
        query_count = query_tracker[(client_ip, qname)]
        print(f"Received query from {client_ip} for: {qname} ({qtype}) -> {ip_address} (Query count: {query_count})")

        reply = DNSRecord(DNSRecord.header(request), q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        sock.sendto(reply.pack(), self.client_address)

class DNSTCPHandler(socketserver.BaseRequestHandler):
    """DNSHandler class to handle incoming DNS requests over TCP."""
    def handle(self):
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



async def handle_dns_request(reader, writer):
    '''Handle incoming DNS requests asynchronously.'''
    try:
        data = await reader.read(512)
        request = DNSRecord.parse(data)

        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        print(f"[!]Parsed DNS request: {qname} :: ({qtype})")
        logger.info(f"Parsed DNS request: {qname} :: ({qtype})")


        ip_address = DOMAIN_IP_MAP.get(qname, "192.168.1.1")
        reply = DNSRecord(DNSRecord.header(request), q=request.q)
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip_address), ttl=60))
        # Log the query and response

        log_query(writer.get_extra_info('peername')[0], qname, ip_address)
        query_count = query_tracker[(writer.get_extra_info('peername')[0], qname)]
        print(f"Received query from {writer.get_extra_info('peername')[0]} for: {qname} ({qtype}) -> {ip_address} (Query count: {query_count})")
        # Send the response

        writer.write(reply.pack())
        await writer.drain()
    except Exception as e:
        logger.error(f"Failed to handle DNS request: {e}")
        print(f"Failed to handle DNS request: {e}")
        writer.close()

async def main():
    server = await asyncio.start_server(handle_dns_request, '0.0.0.0', port)
    async with server:
        await server.serve_forever()

asyncio.run(main())