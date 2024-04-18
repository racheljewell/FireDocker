import argparse
import json

import PythonFolder.docker_list as docker_list
import PythonFolder.docker_requests as docker_requests

def create_container(filepath):
    json_data = load_json(filepath)
    if json_data:
        docker_requests.create_container(json_data)

def create_image(filepath):
    json_data = load_json(filepath)
    if json_data:
        docker_requests.create_image(json_data)

def delete_image(image_name):
    docker_requests.delete_image(image_name)

def load_json(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: JSON file '{filepath}' does not exist.")
        return None

def list_images_and_containers():
    print("Images:")
    docker_list.docker_list_images("/v1.40/images/json")
    print("\nContainers:")
    docker_list.docker_list_containers("/v1.40/containers/json?all=1")

def main():
    parser = argparse.ArgumentParser(description='Example script with multiple required arguments')
    
    parser.add_argument('--create', help='Create a container with JSON file', metavar='JSON_PATH') 
    parser.add_argument('--create-image', help='Create an image with JSON file', metavar='JSON_PATH') 
    parser.add_argument('--delete-image', help='Delete a Docker image by name', metavar='IMAGE_NAME') 
    parser.add_argument('--start', help='Start a Docker container', metavar='CONTAINER_NAME')
    parser.add_argument('--stop', help='Stop a Docker container by name', metavar='CONTAINER_NAME')
    parser.add_argument('--rename', help='Rename a Docker container', nargs=2, metavar=('OLD_NAME', 'NEW_NAME'))
    parser.add_argument('--delete', help='Delete a Docker container by name', metavar='CONTAINER_NAME')
    parser.add_argument('--list', help='List Docker images and containers', action='store_true')
    
    args = parser.parse_args()
    
    if args.create:
        create_container(args.create)
    if args.create_image:
        create_image(args.create_image)
    elif args.delete_image:
        delete_image(args.delete_image)
    elif args.start:
        docker_requests.start_container(container_name=args.start)
    elif args.stop:
        docker_requests.stop_container(container_name=args.stop)
    elif args.rename:
        old_name, new_name = args.rename
        docker_requests.rename_container(old_container_name=old_name, new_container_name=new_name)
    elif args.delete:
        docker_requests.delete_container(container_name=args.delete)
    elif args.list:
        list_images_and_containers()
    else:
        parser.error("Error: At least one action is required.")

if __name__ == '__main__':
    main()
