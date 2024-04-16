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
        # Read the response header
        while b'\r\n\r\n' not in response_data:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response_data += chunk
        
        print("Received header:", response_data.decode())  # Debug print
        
        # Extract response header and remove it from response_data
        header, _, response_data = response_data.partition(b'\r\n\r\n')
        
        print("Header:", header)  # Debug print
        
        # Now process the chunks if there's more data
        if response_data:
            while True:
                # Read the chunk size
                chunk_size_str, _, response_data = response_data.partition(b'\r\n')
                print("Chunk size:", chunk_size_str)  # Debug print
                chunk_size = int(chunk_size_str.strip(), 16)
                if chunk_size == 0:
                    break
                # Read the chunk data
                chunk_data = response_data[:chunk_size]
                response_data = response_data[chunk_size + 2:]  # Skip \r\n after chunk data
                response_data += chunk_data
        
        print("Final response:", response_data.decode())  # Debug print
        return response_data.decode()


    except Exception as e:
        print("Error:", e)  # Debug print
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




print(send_request('/containers/create', method='POST', data=json.dumps(data)))
#print(docker_list('/v1.40/containers/json?all=1'))
print("DONE")