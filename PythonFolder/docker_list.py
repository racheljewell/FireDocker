import socket
import json


debug = False

"""

TODO: 
    ADD PARSER FOR ALL RESPONSES TO SHOW JUST
    1) Name
    2) ID
    3) Maybe some other import info for each response

    4) Prob will have to have a custom parser so that
       for each end of a response 
       parse it and remove theese key value pairs

"""


def docker_list(path=None, method='GET'):

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
            #temp = response_data
            response_data += chunk

            if debug: 
                print("Received chunk:", response_data.decode())  # Debug print
        
            if response_data.endswith(b'0\r\n\r\n'):
               # response_data = temp
                break
        response_str = response_data.decode()
        # print(response_str)
        headers, body = response_str.split('\r\n\r\n', 1)
        first_bracket_index = body.find("[")
        last_bracket_index = body.rfind("]")
        json_content = body[first_bracket_index:last_bracket_index + 1]
        # print(json_content)
        containers = json.loads(json_content)
        # print(containers)
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
