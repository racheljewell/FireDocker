import json

"""
- need to make changes to this code
a) the last line should write a new file named json_cleaned or some variation of the file name and cleaned
b) does not need to clean all key value pairs just most important ones like image for now
c) file name should be changed to something 


"""

def remove_dict_elements(data1, data2):
#    print("Here in dict ...")
#    print(f"Data1: {data1}")
#    print(f"Data2: {data2}") 
  
    common_keys = set(data1.keys()) & set(data2.keys())
    for key in common_keys:
#        print(f"Key: {key}")
        if isinstance(data1[key], dict):
#            print("dict case ...")
            remove_dict_elements(data1[key], data2[key])
        elif isinstance(data1[key], list): 
#            print("list case ...")
            remove_list_elements(data1[key], data2[key])
        elif data1[key] == data2[key]: 
            del data2[key]

def remove_list_elements(data1, data2):
#    print("Here in list ...")
#    print("JSON A:", data1, "\nJSON B:", data2)
#    print("Common Elements:", list(set(data1) & set(data2)))

    dict_in_data1 = any(isinstance(item, dict) for item in data1)
    dict_in_data2 = any(isinstance(item, dict) for item in data2)
    
    if dict_in_data1 and dict_in_data2:
        for idx1, dict1 in enumerate(data1):
            for idx2, dict2 in enumerate(data2):
                remove_dict_elements(data1[idx1], data2[idx2])

    else:
        common_elements = list(set(data1) & set(data2))

        for ele in common_elements:
    #            print(f"Element: {ele}")
            if isinstance(ele, dict) or isinstance(ele, list):
                if isinstance(data1[ele], dict):
    #                print("dict case ...")
                    remove_dict_elements(data1[ele], data2[ele])
                elif isinstance(data1[ele], list):
    #                print("list case ...")
                    remove_list_elements(data1[ele], data2[ele])
            else:
    #            print(f"Removing {ele} ...")
                data2.remove(ele)


# Load JSON data from file1
with open("config_restrictions.json", 'r') as f:
    json_a_result = json.load(f)

# Load JSON data from file2
with open("config_test.json", 'r') as f:
    json_b_result = json.load(f)

"""
## Output json_a_result and json_b_result before removal of common elements
#print("json_a_result before removal:", json_a_result, "\n")
#print("json_b_result before removal:", json_b_result, "\n")
#
## Remove common elements from json_a_result
#remove_dict_elements(json_a_result, json_b_result)
#print("")
#
## Output json_a_result and json_b_result after removal of common elements
#print("json_a_result after removal:", json_a_result, "\n")
#print("json_b_result after removal:", json_b_result)
#
### Add elements that appears in json_a_result but not json_b_result
##add_dict_elements(json_a_result, json_b_result)
##print("")
"""
# Open the same JSON file in write mode
with open("config_test.json", 'w') as file:
    json.dump(json_b_result, file, indent=4)  # Write the modified data back to the file, overwriting its content
