import json
import re
import socket
import PythonFolder.config_parser as config_parser
import PythonFolder.logger as logger

debug = False

class NoImageFound(Exception):
    pass


"""
All functions should reformat to 
- send path
- send data
- method should be defaulted 

- use the build request function to build the request

"""
"""
This is where the oop stuff comes in? 

instead of passing parameters, pass objects that contain the
params you want 

like a reqeust object that you can get request.path or request.method 
from

and each request will have an obj? 

but if each has the obj

where do you build them? : the constructor? 
and then call methods like build request? 

so does each requst inheiret some superclass like requests

"""

def buildRequest(path=None, method='GET', data=None): 
    request = f'{method} {path} HTTP/1.1\r\n'
    request += 'Host: unix\r\n'
    request += 'Content-Type: application/json\r\n'

def create_container(path='/containers/create', method='POST', data=""):
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
            data = json.dumps(config_parser.restrict(data))

            if "Image" not in data: 
                if debug: 
                    print(data)
                
                raise NoImageFound
            
           # print(data)
            request += f'Content-Length: {len(data)}\r\n'
            request += '\r\n'
            request += data
        
        if debug: 
            print("This is a requst \n" + request)


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

            # Check if we received the terminating chunk '0\r\n\r\n'
            if response_data.endswith(b'0\r\n\r\n'):
                response_data = temp
                break

        response_str = response_data.decode()
        
        headers, body = response_str.split('\r\n\r\n', 1)

        statusCode = int(headers[9:12])

        log = logger.Logger()
        log.log_message(statusCode, "Creating Container")

        return response_data.decode()
    
    except NoImageFound: 
        print("Image Restricted")
        return False
    
    finally:
        # Close the socket before exiting the function entirely!
        sock.close()

def delete_container(path='/containers/', method='DELETE',container_name=""):
    # Create a Unix domain socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        # Connect to the Docker Unix socket
        sock.connect('/var/run/docker.sock')
        
        # Prepare the HTTP request to delete the container by name
        path = f'/containers/{container_name}'
        method = 'DELETE'
        
        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        request += '\r\n'
        
        if debug: 
            print("This is a request:\n" + request)

        # Send the request
        sock.sendall(request.encode())
        
        # Receive the response
        
        response_data = sock.recv(4096)
        
        response_str = response_data.decode()
        
        headers, body = response_str.split('\r\n\r\n', 1)
        statusCode = int(headers[9:12])
        log = logger.Logger()
        log.log_message(statusCode, "Deleting Container")
        return response_data
    
    finally:
        # Close the socket
        sock.close()

def stop_container(path='/containers/', method='POST',container_name=""):
    # Create a Unix domain socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        # Connect to the Docker Unix socket
        sock.connect('/var/run/docker.sock')
        
        # Prepare the HTTP request to delete the container by name
        path = f'/containers/{container_name}/stop'
        method = 'POST'
        
        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        request += '\r\n'
        
        if debug: 
            print("This is a request:\n" + request)

        # Send the request
        sock.sendall(request.encode())
        
        # Receive the response
        
        response_data = sock.recv(4096)
        response_str = response_data.decode()
        
        headers, body = response_str.split('\r\n\r\n', 1)
        statusCode = int(headers[9:12])
        log = logger.Logger()
        log.log_message(statusCode, "Stopping Container")
        
        return response_data
    
    finally:
        # Close the socket
        sock.close()

def start_container(path='/containers/', method='POST',container_name=""):
    # Create a Unix domain socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        # Connect to the Docker Unix socket
        sock.connect('/var/run/docker.sock')
        
        # Prepare the HTTP request to delete the container by name
        path = f'/containers/{container_name}/start'
        method = 'POST'
        
        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        request += '\r\n'
        
        if debug: 
            print("This is a request:\n" + request)

        # Send the request
        sock.sendall(request.encode())
        
        # Receive the response
        
        response_data = sock.recv(4096)
        
        response_str = response_data.decode()
        
        headers, body = response_str.split('\r\n\r\n', 1)
        statusCode = int(headers[9:12])
        log = logger.Logger()
        log.log_message(statusCode, "Starting Container")

        if statusCode == 304: 
            print("\033[31mDocker image already in requested state.\033[0m")
        
        return response_data
    
    finally:
        # Close the socket
        sock.close()

def rename_container(old_container_name="", new_container_name=""):
    # Create a Unix domain socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        # Connect to the Docker Unix socket
        sock.connect('/var/run/docker.sock')
        
        # Prepare the HTTP request to delete the container by name
        path = f'/containers/{old_container_name}/rename?name={new_container_name}'
        method = 'POST'
        
        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        request += '\r\n'
        
        if debug: 
            print("This is a request:\n" + request)

        # Send the request
        sock.sendall(request.encode())
        
        # Receive the response
        
        response_data = sock.recv(4096)
        response_str = response_data.decode()
        
        headers, body = response_str.split('\r\n\r\n', 1)
        statusCode = int(headers[9:12])
        log = logger.Logger()
        log.log_message(statusCode, "Renaming Container")
        return response_data
        
        return response_data
    
    finally:
        # Close the socket
        sock.close()

def json_parser(strContaingJson): 
    match = re.search(r'\{(.+?)\}', strContaingJson, re.DOTALL)
    if match:
        json_data = match.group(1)  # Extract the matched content
        print(json_data)

    else:
        print("No JSON data found in the response.")

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
   
