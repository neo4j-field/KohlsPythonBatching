import json
import os
from functools import reduce,wraps
from neo4j import GraphDatabase,debug
from transactionfunctions import create_product,create_sku
import itertools




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






def get_sku(json,*keys):
    '''
    Function that traverses deep into a dictionary
    https://stackoverflow.com/questions/25833613/safe-method-to-get-value-of-nested-dictionary

    :param json: json object
    :param keys: variable length args that represent the keys to traverse.
    :return:
    '''
    return reduce(lambda d, key: d.get(key) if d else None,keys,json)



def ship_parameters(func):
    '''
    Decorator function that wraps the collection (list of maps) in another map to make compatiable with Neo4j transaction functions.
    :param func: parameter generator functions
    :return: dictionary: key = 'batch', value = list of maps
    '''
    @wraps(func)
    def wrap(*args, **kw):
        results = func(*args,**kw)
        dict = {'batch':results}
        return dict
    return wrap



@ship_parameters
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


@ship_parameters
def get_sku_properties(skus):
    '''
    get sku properties. I'm grabbing every property if the value in the key,pair is a string. (my logic is if it is a dict
    we are going to be grabbing it later as a seperate node.
    :param skus:
    :return:
    '''
    sku_properties = []
    for sku in skus:
        skus_parameters = {sku_key:sku_val for sku_key,sku_val in sku.items() if isinstance(sku_val,str)}
        sku_properties.append(skus_parameters)
    return sku_properties



def get_selling_channel_properties(sku):
    '''
    This doesn't follow the correct format. I don't know how to handle this data structure...
    :param sku:
    :return:
    '''
    for sku in skus:
        selling_channel_parameters = {sku_key:sku_val for sku_key,sku_val in sku.items() if sku_key == 'sellingChannels'}
        unpacked_selling_channel_parameters = [{'sellingChannels':val_elem} for val_elem in selling_channel_parameters['sellingChannels']]
        return unpacked_selling_channel_parameters


def get_omni_channel_properties(sku):
    '''
    This doesn't follow the correct format. I don't know how to handle this data structure...

    :param sku:
    :return:
    '''
    for sku in skus:
        omni_channel_parameters = {sku_key:sku_val for sku_key,sku_val in sku.items() if sku_key == 'omniChannels'}
        unpacked_omni_channel_parameters = [{'omniChannels':val_elem} for val_elem in omni_channel_parameters['sellingChannels']]
        return unpacked_omni_channel_parameters





if __name__ == '__main__':



    sample_input = r'/Users/alexanderfournier/PycharmProjects/KohlsDataModel/resources/data/product_graphql_response.json'
    directory = r'/Users/alexanderfournier/PycharmProjects/KohlsDataModel/resources/data'
    acceptable_product_properties = ['id','title','variations','altTag','description','brand']
    sku_keys = ('data','product','skus')

    auth = ('neo4j', 'Z3NgZwK0JuVMysRpLfgKI8M2S9hGjfzu_iC3CU1ABvM')
    uri = 'neo4j+s://fba1c714.databases.neo4j.io'
    driver = GraphDatabase.driver(uri, auth=auth)




    json_objects = get_json_objects(directory)


    for json in json_objects:
        product_properties = get_product_properties(json,acceptable_product_properties)
        skus = get_sku(json,*sku_keys)
        sku_properties = get_sku_properties(skus)
        selling_channel = get_selling_channel_properties(skus)






    with driver.session() as session:
        session.write_transaction(create_sku,sku_properties)
        session.write_transaction(create_product,product_properties)
    driver.close()





















