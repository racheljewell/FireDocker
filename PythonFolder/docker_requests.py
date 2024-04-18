import json
import re
import socket
import docker
import os

debug = False

def create_container(path=None, method='GET', data=None):
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
    
    finally:
        # Close the socket
        sock.close()

def create_image(json_data):
    client = docker.from_env()
    try:
        image, cmd, env = json_data['Image'], json_data['Cmd'], json_data['Env']
        
        # Define a temporary Dockerfile content based on provided commands and environment variables
        dockerfile_content = f"FROM {image}\nCMD {cmd}\nENV {env}"
        
        # Write the Dockerfile content to a temporary file
        dockerfile_path = 'Dockerfile'
        with open(dockerfile_path, 'w') as dockerfile:
            dockerfile.write(dockerfile_content)
        
        # Build the image using the Dockerfile
        build_result = client.images.build(path='.', tag=image, dockerfile=dockerfile_path)
        
        for build_log in build_result[1]:
            print(build_log)
        print(f"Image '{image}' created successfully.")
    except KeyError:
        print("Error: JSON format does not match expected structure for image creation.")
    finally:
        # Clean up: remove the temporary Dockerfile
        if os.path.exists(dockerfile_path):
            os.remove(dockerfile_path)

def delete_image(image_name):
    client = docker.from_env()
    try:
        client.images.remove(image=image_name)
        print(f"Image '{image_name}' deleted successfully.")
    except docker.errors.APIError as e:
        print(f"Error deleting image '{image_name}': {e}")

def delete_container(container_name):
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

def stop_container(container_name):
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

def start_container(container_name):
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
        return response_data
    
    finally:
        # Close the socket
        sock.close()

def rename_container(old_container_name, new_container_name):
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
   
