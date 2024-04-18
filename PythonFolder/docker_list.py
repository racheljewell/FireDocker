import socket
import json

debug = False

def docker_list_images(path=None, method='GET'):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        sock.connect('/var/run/docker.sock')

        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        request += '\r\n'

        sock.sendall(request.encode())

        response_data = b''
        while True:
            chunk = sock.recv(4096)

            if not chunk:
                break

            response_data += chunk

            if response_data.endswith(b'0\r\n\r\n'):
                break

        response_str = response_data.decode()
        headers, body = response_str.split('\r\n\r\n', 1)
        first_bracket_index = body.find("[")
        last_bracket_index = body.rfind("]")
        json_content = body[first_bracket_index:last_bracket_index + 1]

        images = json.loads(json_content)

        print("{:<30}\t{:<30}".format("IMAGE_NAME", "IMAGE_ID"))
        for image in images:
            name = image.get("RepoTags")[0].split(':')[0]
            id = image.get("Id")[:12]
            
            print("{:<30}\t{:<30}".format(name, id))

        return response_data.decode()

    except Exception as e:
        return str(e)

    finally:
        sock.close()

def docker_list_containers(path=None, method='GET'):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        sock.connect('/var/run/docker.sock')

        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        request += '\r\n'

        sock.sendall(request.encode())
        
        response_data = b''
        while True:
            chunk = sock.recv(4096)

            if not chunk:
                break
            response_data += chunk

            if debug: 
                print("Received chunk:", response_data.decode())  # Debug print
        
            if response_data.endswith(b'0\r\n\r\n'):
                break
        response_str = response_data.decode()
        headers, body = response_str.split('\r\n\r\n', 1)
        first_bracket_index = body.find("[")
        last_bracket_index = body.rfind("]")
        json_content = body[first_bracket_index:last_bracket_index + 1]
        
        containers = json.loads(json_content)

        print("{:<20}\t{:<20}\t{:<20}\t{:<20}".format("CONTAINER_NAME", "CONTAINER_ID", "IMAGE", "STATUS"))
        for container in containers:
            name = container.get("Names")[0].strip('/')
            id = container.get("Id")[:12]
            image = container.get("Image")
            status = container.get("Status")
            
            print("{:<20}\t{:<20}\t{:<20}\t{:<20}".format(name, id, image, status))

        return response_data.decode()

    except Exception as e:
        return str(e)
    
    finally: 
        sock.close()


if debug: 
    print(docker_list('/v1.40/containers/json?all=1'))
