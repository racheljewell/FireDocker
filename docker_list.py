import socket

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
        
            if response_data.endswith(b'0\r\n\r\n'):
                break

        return response_data.decode()

        
    except Exception as e:
        return str(e)
    
    finally: 
        sock.close()


"""

Route for list command


"""

print(docker_list('/v1.40/containers/json?all=1'))
