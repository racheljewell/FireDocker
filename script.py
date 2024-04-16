import argparse
import json

import docker_list
import docker_requests
"""
TODO: 
- rm the demo json
- rm the other untracked json files from cache

git rm --cache <filename>

"""

def create_func(filepath):
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
    parser.add_argument('--list', help='List something without a JSON file', action='store_true')
    # Add more arguments as needed
    
    args = parser.parse_args()
    
    json_string = ""
    # Access the arguments using args.create, args.list, etc.
    if args.create:
        json_string = create_func(args.create)
        docker_requests.json_parser(docker_requests.create_container(path='/containers/create', method='POST', data=json_string))
        print(json_string)
    elif args.list:
        print(docker_list.docker_list("/v1.40/containers/json?all=1"))
    else:
        parser.error("Error: At least one action is required. Use --create or --list.")

if __name__ == '__main__':
    main()
