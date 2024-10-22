# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:08:32 2023

@author: avacy
"""
import asyncio
import socket
import ipaddress

def read_myhosts(file_path):
    hosts = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                parts = line.split()
                ip_address_str, *domains = parts
                ip_address = ipaddress.ip_address(ip_address_str)
                for domain in domains:
                    hosts[domain] = ip_address
    return hosts

def get_transaction_id(data):
    return data[0] << 8 | data[1]

def get_qclass(data):
    index = 12
    while data[index] != 0:
        label_length = data[index]
        index += 1
        index += label_length
    index += 1
    index += 2
    qclass = int.from_bytes(data[index:index + 2], byteorder='big')

    return qclass


def parse_dns_query(data):
    query_domain = ""
    index = 12
    transaction_id = get_transaction_id(data)
    while data[index] != 0:
        label_length = data[index]
        index += 1
        query_domain += data[index:index + label_length].decode("utf-8") + "."
        index += label_length
    return query_domain.rstrip("."), transaction_id

class DNSResolverProtocol(asyncio.DatagramProtocol):
    def __init__(self, loop, hosts):
        self.loop = loop
        self.hosts = hosts
        
    def send_error_response(self, transaction_id, error_code, ip_address):
        response = bytearray()
        response.extend(transaction_id.to_bytes(2, byteorder='big'))  # transaction ID
        response.extend((0x8000 | error_code).to_bytes(2, byteorder='big'))  # flags with error code
        response.extend(b'\x00\x01')  # questions
        response.extend(b'\x00\x01')  # answer 
        response.extend(b'\x00\x00')  # authority
        response.extend(b'\x00\x00')  # additional 
        
        return response      
    
    def create_dns_response(self, query_domain, transaction_id):
        ip_address = self.hosts.get(query_domain, "0.0.0.0")

        response = bytearray()
        response.extend(transaction_id.to_bytes(2, byteorder='big'))  # transaction ID
        response.extend(b'\x81\x80')  # flags
        response.extend(b'\x00\x01')  # questions
        response.extend(b'\x00\x01')  # answer 
        response.extend(b'\x00\x00')  # authority 
        response.extend(b'\x00\x00')  # additional 

        for part in query_domain.split('.'):
            response.append(len(part))
            response.extend(part.encode())

        response.extend(b'\x00')  # end of domain
        response.extend(b'\x00\x01')  # type (A record)
        response.extend(b'\x00\x01')  # class (IN)
        response.extend(b'\xc0\x0c')  # name pointer to domain
        response.extend(b'\x00\x01')  # type (A record)
        response.extend(b'\x00\x01')  # class (IN)
        response.extend(b'\x00\x00\x00\x10')  # TTL (16 seconds)
        response.extend(b'\x00\x04')  
        response.extend(socket.inet_aton(str(ip_address)))

        return response
    
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f"query has received from {addr}")
        asyncio.create_task(self.handle_dns_query(data, addr))

    async def handle_dns_query(self, data, addr):
        query_domain, transaction_id = parse_dns_query(data)
        qc = get_qclass(data)
        
        if qc == 1:
             if query_domain in self.hosts:
                 response_data = self.create_dns_response(query_domain, transaction_id)
                 ip_address = self.hosts[query_domain]
                 self.transport.sendto(response_data, addr)
                 print(f"Response has been sent to {addr}")
             else:
                 error_response = self.send_error_response(transaction_id, 3, ipaddress.ip_address("0.0.0.0"))
                 self.transport.sendto(error_response, addr)
                 print("The domain does not exist")
        else:
            print("Not Implemented")
            error_response = self.send_error_response(transaction_id, 4, ipaddress.ip_address("0.0.0.0"))
            self.transport.sendto(error_response, addr)



async def main():
    HOST = '::'
    PORT = 5353

    hosts = read_myhosts('/etc/myhosts')

    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: DNSResolverProtocol(loop, hosts),
        local_addr=(HOST, PORT))

    print(f"DNS resolver is listening on {HOST}:{PORT}...")

    try:
        await asyncio.sleep(3600) 
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())
