import json
import os
from functools import reduce
from neo4j import GraphDatabase
from pprint import pprint


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



def get_product_properties(json,acceptable_product_properties):
    '''
    traverses json objects to retrieve product keys and values.
    :param json: json object
    :param acceptable_product_properties: list of acceptable properies to grab
    :return:
    '''
    product_parameters = []
    for data in json.values():
        for product_key, product_vals in data.items():
            parameter = {k:v for k,v in product_vals.items() if k in acceptable_product_properties}
            product_parameters.append(parameter)
    return product_parameters


def get_sku(json,*keys):
    '''
    Function that traverses deep into a dictionary
    https://stackoverflow.com/questions/25833613/safe-method-to-get-value-of-nested-dictionary

    :param json: json object
    :param keys: variable length args that represent the keys to traverse.
    :return:
    '''
    return reduce(lambda d, key: d.get(key) if d else None,keys,json)


def get_sku_properties(skus):
    sku_properties = []
    for sku in skus:
        pprint(sku)
        for sku_key,sku_value in sku.items():
            if isinstance(sku_value,str):
                sku_properties.append(sku)

    return sku_properties
















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


    auth = ('neo4j','Z3NgZwK0JuVMysRpLfgKI8M2S9hGjfzu_iC3CU1ABvM')
    uri = 'neo4j+s://fba1c714.databases.neo4j.io'
    sample_input = r'/Users/alexanderfournier/PycharmProjects/KohlsDataModel/resources/data/product_graphql_response.json'
    directory = r'/Users/alexanderfournier/PycharmProjects/KohlsDataModel/resources/data'
    acceptable_product_properties = ['id','title','variations','altTag','description','brand']
    sku_keys = ('data','product','skus')
    driver = GraphDatabase.driver(uri, auth=auth)













    json_objects = get_json_objects(directory)


    for json in json_objects:
        product_properties = get_product_properties(json,acceptable_product_properties)
        skus = get_sku(json,*sku_keys)
        get_sku_properties(skus)






















