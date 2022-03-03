import json


def create_product_and_sku(tx,batch):
    tx.run(
    '''
    UNWIND $batch as param
    MERGE (c:Contract {id:param._Contract__contract_id,cost:param._Contract__price})
    WITH param,c
    MATCH (cat:Category {id:param._Contract__car_category})
    MERGE (c) - [:INCLUDES] -> (cat)
    ''',parameters=batch)



def create_



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









file = r'/Users/alexanderfournier/Downloads/Java-Batch/src/resources/product_graphql_response.json'
open_file_read_schema(file)
