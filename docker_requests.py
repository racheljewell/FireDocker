import json
import re
import socket
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')


debug = False

def create_container(path=None, method='GET', data=None):
    # logging...
    logging.debug(f"Creating container with path: {path}, method: {method}, data: {data}")

    # Create a Unix domain socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        # Connect to the Docker Unix socket
        sock.connect('/var/run/docker.sock')
        
        # Prepare the HTTP request
        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        
        if data:
            request += f'Content-Length: {len(data)}\r\n'
            request += '\r\n'
            request += data
        
        if debug: 
            print("This is a requst \n" + request)

        # logging...
        logging.debug(f"Request prepared: {request}")

        # Send the request
        sock.sendall(request.encode())
         # Receive the response
        response_data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            temp = response_data
            response_data += chunk
            #print("Received chunk:", response_data.decode())  # Debug print

            # logging...
            logging.debug(f"Received chunk: {response_data.decode()}")
            
            # Check if we received the terminating chunk '0\r\n\r\n'
            if response_data.endswith(b'0\r\n\r\n'):
                response_data = temp
                break
        return response_data.decode()
    
    finally:
        # Close the socket
        sock.close()

        # logging...
        logging.debug("Socket closed.")

def json_parser(strContaingJson): 
    match = re.search(r'\{(.+?)\}', strContaingJson, re.DOTALL)
    if match:
        json_data = match.group(1)  # Extract the matched content
        print(json_data)

        # logging...
        logging.debug(f"Extracted JSON data: {json_data}")
    else:
        print("No JSON data found in the response.")

        # logging...
        logging.warning("No JSON data found in the response.")

# Debug data
data = {
    "Image": "mysql:latest",
    "Cmd": ["mysqld"],
    "Env": ["MYSQL_ROOT_PASSWORD=my-secret-pw"],
    "HostConfig": {
        "PortBindings": {
            "3306/tcp": [{"HostPort": "3306"}]
        }
    }
}


if debug:
    response_string_container = create_container('/containers/create', method='POST', data=json.dumps(data))
    json_parser(response_string_container)
   
