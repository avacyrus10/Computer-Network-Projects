# Reliable UDP Communication

This project implements a reliable UDP communication between a client and server using sequence numbers, acknowledgments (ACKs), and a sliding window to ensure reliable and ordered packet transmission over a potentially lossy network.

## Components

The communication flow is as follows:
1. The **ncat client** sends data to the intermediary client through port `1111`.
2. The **intermediary client** forwards the received data over a lossy link on port `12345`.
3. The data is then redirected to port `54321`, where the intermediary server receives it.
4. After ensuring the correct order of the data, the intermediary server forwards the data to the **ncat server** on port `54322`.

## Key Features

- **Reliable Transmission**: Using acknowledgments (ACKs), the system ensures reliable transmission of data.
- **Ordered Delivery**: Sequence numbers ensure that packets are delivered to the ncat server in the correct order.
- **Sliding Window**: The sliding window mechanism helps manage unacknowledged packets and control the flow of data between the sender and receiver.

## Flow

- The `run_my_server` and `run_my_client` functions set up UDP sockets and start threads for sending and receiving data.
- **Sender threads**: These threads send data while respecting the window sizes and ACKs received from the receiver.
- **Receiver threads**: These threads receive data, process the ACKs, and handle out-of-order packets by storing them in a queue until they can be processed in the correct order.

## Usage

To set up and run the system, use the following steps:

1. **Start the ncat server** (for receiving data):
  ```bash
   ncat --recv-only -u -l 54322
   ```
2. **Start the ncat client** (for sending data):

  ```bash
   seq 1000 | { while read; do sleep 0.01; echo "$REPLY"; done;} | ncat --send-only -u 127.0.0.1 1111
   ```
3. **Start the lossy link**:
 ```bash
    ./lossy_link-linux 127.0.0.1:12345 127.0.0.1:54321
   ```
This setup will ensure that the data sent from the ncat client is forwarded reliably to the ncat server, even if the network link is lossy.
   
   

