import argparse
import json
import docker
import os
import PythonFolder.docker_list as docker_list
import PythonFolder.docker_requests as docker_requests

def create_func(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)

        # Convert Cmd and Env arrays to strings if needed
        if isinstance(data.get('Cmd'), list):
            data['Cmd'] = data['Cmd'][0] if data['Cmd'] else ''
        if isinstance(data.get('Env'), list):
            data['Env'] = data['Env'][0] if data['Env'] else ''

        return data
    except FileNotFoundError:
        print(f"Error: JSON file '{filepath}' does not exist.")
        return None


def build_image(image_info):
    client = docker.from_env()
    try:
        image, cmd, env = image_info['Image'], image_info['Cmd'], image_info['Env']
        
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

def create_image(filepath):
    image_data = create_func(filepath)
    if image_data:
        build_image(image_data)

def main():
    parser = argparse.ArgumentParser(description='Example script with multiple required arguments')
    
    parser.add_argument('--create', help='Create a container with JSON file', metavar='JSON_PATH') 
    parser.add_argument('--create-image', help='Create an image with JSON file', metavar='JSON_PATH') 
    parser.add_argument('--start', help='Start a Docker container', metavar='CONTAINER_NAME')
    parser.add_argument('--stop', help='Stop a Docker container by name', metavar='CONTAINER_NAME')
    parser.add_argument('--rename', help='Rename a Docker container', nargs=2, metavar=('OLD_NAME', 'NEW_NAME'))
    parser.add_argument('--delete', help='Delete a Docker container by name', metavar='CONTAINER_NAME')
    parser.add_argument('--list', help='List Docker containers', action='store_true')
    # Add more arguments as needed
    
    args = parser.parse_args()
    
    # Access the arguments using args.create, args.list, etc.
    if args.create:
        # Call the create_container function here or other relevant function
        docker_requests.create_container(args.create)
    elif args.create_image:
        create_image(args.create_image)
    elif args.start:
        container_name = args.start 
        docker_requests.start_container(container_name=container_name)
    elif args.stop:
        container_name = args.stop
        docker_requests.stop_container(container_name=container_name)
    elif args.rename:
        old_container_name, new_container_name = args.rename
        docker_requests.rename_container(old_container_name=old_container_name, new_container_name=new_container_name)
    elif args.delete:
        container_name = args.delete
        docker_requests.delete_container(container_name=container_name)
    elif args.list:
        docker_list.docker_list("/v1.40/containers/json?all=1")
    else:
        parser.error("Error: At least one action is required. Use --create, --create-image, or --list.")

if __name__ == '__main__':
    main()
