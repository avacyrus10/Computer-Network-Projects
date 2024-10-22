# DNS Resolver

In this project, I have implemented a DNS resolver that can answer class A queries on port 5353 using Python and the asyncio library.

## How Does It Work?

This DNS resolver listens for incoming DNS queries over UDP and responds with the appropriate IPv4 address if the domain exists in the `/etc/myhosts` file. If the domain does not exist, it returns an error response. Let's go through the key components of the project.

### 1. `read_myhosts(file_path)`
This function reads a custom hosts file (e.g., `/etc/myhosts`) where each line contains an IP address followed by one or more domain names. It returns a dictionary called `hosts` that maps domain names to their equivalent IP addresses.

- The IP addresses are converted to `ipaddress` objects.
- Commented lines and empty lines are ignored.

### 2. `get_transaction_id(data)`
This function extracts the transaction ID from the DNS query. The transaction ID is formed by combining the first two bytes of the DNS packet, which are used to uniquely identify the DNS transaction.

### 3. `get_qclass(data)`
This function extracts the QCLASS of the DNS query, indicating the type of the record being requested (e.g., A, AAAA, etc.).

### 4. `parse_dns_query(data)`
This function parses the domain name from the DNS query. It starts reading at byte 12 (after the DNS header) and reads each label in the domain name. The domain name and the transaction ID are returned.

### 5. `DNSResolverProtocol` Class
This class is used to handle DNS queries and send appropriate responses. It inherits from `asyncio.DatagramProtocol` and contains several key methods:

- **`send_error_response(transaction_id, error_code, ip_address)`**: Creates an error response when a domain name does not exist in the `/etc/myhosts` file. It constructs the response using a byte array and adds the transaction ID, flags, and error code.

- **`create_dns_response(query_domain, transaction_id)`**: Creates a valid DNS response for a given query if the domain is found. The response includes the transaction ID, flags, domain name, type (A record), class (IN), TTL, and the IPv4 address.

- **`connection_made(transport)`**: This method is called when a connection is made. It creates a transport object used for communication.

- **`datagram_received(data, addr)`**: This method is called when a DNS query is received. It processes the query and calls `create_dns_response` or `send_error_response` based on whether the domain exists in the hosts file.

- **`handle_dns_query(data, addr)`**: This method asynchronously handles each DNS query received, extracting the query domain and QCLASS, and then sending a response or an error as needed.

### 6. `main()`
The `main` function sets up the DNS resolver server. It reads the hosts file, creates a UDP server on port 5353, and starts the asyncio event loop. The resolver can handle parallel DNS queries using `asyncio.create_task`, which allows it to process multiple queries concurrently.

## How to Run the Project

1. **Setup**:
 - Make sure you have Python 3.x installed.
 - Install the `ipaddress` module if not already available (`pip install ipaddress`).

2. **Hosts file**:
 - Create or update your `/etc/myhosts` file with the required IP addresses and domain names.

3. **Run the server**:
 - You can run the DNS resolver using:
   ```bash
   python3 dns_resolver.py
   ```

4. **Testing**:
 - Use a DNS query tool like `dig` to test the DNS server:
   ```bash
   dig @localhost -p 5353 example.com
   ```

## Key Features

- Handles class A (IPv4) DNS queries.
- Supports parallel handling of DNS requests using asyncio.
- Responds with error messages when a domain does not exist or if the query class is not supported.
- Reads from a customizable hosts file (`/etc/myhosts`).

## Author

Ava Cyrus
[@avacyrus10](https://github.com/avacyrus10)
