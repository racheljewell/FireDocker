import json
import socket

def create_container(path, method='GET', data=None):
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
        
        print(request)
        # Send the request
        sock.sendall(request.encode())
        
        # Receive the response
        response = sock.recv(4096)
        
        # Parse and return the response
        return response.decode()
    
    finally:
        # Close the socket
        sock.close()

"""
handle chunked encoding
"""


def docker_list(path, method='GET'):
    # Create a Unix domain socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        sock.connect('/var/run/docker.sock')

        # Prepare the HTTP request
        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        request += '\r\n'  # End of headers

        # Send the request
        sock.sendall(request.encode())
        
        # Receive the response
        response_data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
            print("Received chunk:", response_data.decode())  # Debug print
            
            # Check if we received the terminating chunk '0\r\n\r\n'
            if response_data.endswith(b'0\r\n\r\n'):
                break
        
        return response_data.decode()


    except Exception as e:
        return str(e)
    
    finally: 
        sock.close()


# Example: Create a container
data = {
    "Image": "python:latest",
    "Cmd": ["mysqld"],
    "Env": ["MYSQL_ROOT_PASSWORD=my-secret-pw"],
    "HostConfig": {
        "PortBindings": {
            "3306/tcp": [{"HostPort": "3306"}]
        }
    }
}




print(create_container('/containers/create', method='POST', data=json.dumps(data)))
print(docker_list('/v1.40/containers/json?all=1'))
print("DONE")