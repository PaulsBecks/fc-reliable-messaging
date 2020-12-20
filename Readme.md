# Fog Computing Reliable Messaging example

This repository simulates a edge client and a cloud server. The server is supposed to listen to incomming traffic. 

The client is supposed to send periodically data to the server. If the server fails or the connection is broken due to other reasons the periodically generated data needs to be buffered. Once the connection is available again, the data needs to be forwarded to the server.

# Setup

Install dependencies.

```bash
pip3 install -r requirements.txt
```

Run the server

```bash
python3 server.py 
```

Run as many clients as you want.


```bash
python3 client.py <client-name>
```
