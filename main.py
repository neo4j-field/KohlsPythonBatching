import json
import os


def get_json_objects(directory:str):
    '''
    Function takes a string that represents the absolute path containing JSON files.
    outputs a List of Json Objects.
    :param directory: Str
    :return: list of json objects
    '''
    paths = [os.path.join(directory,path) for path in os.listdir(directory)]

    json_objects = []
    for file in paths:
        with open(file) as jsonfile:
            data = json.load(jsonfile)
            json_objects.append(data)
    return json_objects


def get_product_label_and_properties(json,acceptable_properties:list):
    '''
    TODO: I really DO NOT like having to explicitly pass a list of acceptable properties.. There has to be a better solution...
    :param json: Json Object
    :param acceptable_properties: list of acceptable paramters for the product
    :return: Dictionary -> key = label, val = list of properties
    '''
    for data in json.values():
        for product_label,product_attributes in data.items():
            label_and_properties = {label:[_property for _property in product_attributes.keys() if _property in acceptable_properties] for label in data.keys()}
    return label_and_properties



def get_product_parameters(json):
    list_of_dict_objects = []

    for data in json.values():
        for product_label,product_attributes in data.items():







def batch_parameters(parameters:list,batch_size:int):
    '''
    Chunks a list into smaller sublists. The idea here is to take create batches or chunks of parameters.
    :param parameters: input parameters
    :param chunk_size: size of sublists
    :return: list of lists. sublists contain a fixed number of elements (the last sublist will just contain the remainder)
    '''
    chunks = (parameters[x:x+batch_size] for x in range(0, len(parameters),batch_size))
    return chunks


def open_file_read_schema(file: str):
    '''

    :param file: Str filepath
    :return: json object
    '''

    with open(file) as f:
        data = json.load(f)
    print(json.dumps(data, indent=4))
    return data



if __name__ == '__main__':


    sample_file = r'/Users/alexanderfournier/PycharmProjects/KohlsDataModel/resources/data/product_graphql_response.json'
    directory = r'/Users/alexanderfournier/PycharmProjects/KohlsDataModel/resources/data'
    json_objects = get_json_objects(directory)


    first_json_object = json_objects[0]
    acceptable_product_properties = ['id','title','variations','altTag','description','brand']
    label_and_properties = get_product_label_and_properties(first_json_object,acceptable_product_properties)
    construct_base_product_cypher(label_and_properties)







