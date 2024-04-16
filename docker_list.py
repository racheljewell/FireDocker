import socket
import logging


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


# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')



def docker_list(path=None, method='GET'):
    # logging ...
    logging.debug(f"Requesting Docker list with path: {path} and method: {method}")


    # Create a Unix domain socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    try:
        sock.connect('/var/run/docker.sock')

        # Prepare the HTTP request
        request = f'{method} {path} HTTP/1.1\r\n'
        request += 'Host: unix\r\n'
        request += 'Content-Type: application/json\r\n'
        request += '\r\n'  # End of headers

        # logging...
        logging.debug(f"Sending request: {request}")

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

            # logging...
            logging.debug(f"Received chunk: {response_data.decode()}")

            if debug: 
                print("Received chunk:", response_data.decode())  # Debug print
        
            if response_data.endswith(b'0\r\n\r\n'):
               # response_data = temp
                break

        return response_data.decode()

        
    except Exception as e:
        # logging...
        logging.error("Failed to list Docker containers", exc_info=True)

        return str(e)
    
    finally: 
        sock.close()

        # logging...
        logging.debug("Socket closed.")


if debug: 
    print(docker_list('/v1.40/containers/json?all=1'))
