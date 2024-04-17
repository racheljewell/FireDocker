import argparse
import json

import PythonFolder.docker_list as docker_list
import PythonFolder.docker_requests as docker_requests
"""
TODO: 
- rm the demo json
- rm the other untracked json files from cache

git rm --cache <filename>

"""


def jsonfile_to_data(filepath):
    json_string = "{}"
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        json_string = json.dumps(data)
    except:
        print(f"Error: JSON file '{filepath}' does not exist.")
    return json_string

def list_func():
    print("List function ...")

def main():
    parser = argparse.ArgumentParser(description='Example script with multiple required arguments')
    
    parser.add_argument('--create', help='Create something with JSON file', metavar='JSON_PATH') # Requires JSON path
    parser.add_argument('--start', help='Start a Docker container', metavar='CONTAINER_NAME')
    parser.add_argument('--stop', help='Stop a Docker container by name', metavar='CONTAINER_NAME')
    parser.add_argument('--rename', help='Rename a Docker container', nargs=2, metavar=('OLD_NAME', 'NEW_NAME'))
    parser.add_argument('--delete', help='Delete a Docker container by name', metavar='CONTAINER_NAME')
    parser.add_argument('--list', help='List something without a JSON file', action='store_true')
    # Add more arguments as needed
    
    args = parser.parse_args()
    
    json_string = ""
    # Access the arguments using args.create, args.list, etc.
    if args.create:
        json_string = jsonfile_to_data(args.create)
        docker_requests.json_parser(docker_requests.create_container(path='/containers/create', method='POST', data=json_string))
        print(json_string)
    elif args.start:
        container_name = args.start 
        docker_requests.start_container(container_name=container_name)
    elif args.stop:
        container_name = args.stop
        docker_requests.stop_container(container_name=container_name)
        # Implement container stoppage
    elif args.rename:
        old_container_name, new_container_name = args.rename
        docker_requests.rename_container(old_container_name=old_container_name, new_container_name=new_container_name)
        # Implement container renamage
    elif args.delete:
        container_name = args.delete
        docker_requests.delete_container(container_name=container_name)
        # Implement container deletage
    elif args.list:
        docker_list.docker_list("/v1.40/containers/json?all=1")
    else:
        parser.error("Error: At least one action is required. Use --create or --list.")

if __name__ == '__main__':
    main()
