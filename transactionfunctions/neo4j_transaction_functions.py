



def create_product_and_sku(tx,batch):
    tx.run(
    '''
    UNWIND $batch as param
    MERGE (p:Product {title:param.title,variation:param.variation,altTag:param.altTag,description:param.description,brand:param.brand})
    WITH param,p
    MERGE (s:SKU {id:param.id,colorFamily:param.colorFamily,displayColor:param.displayColor,vendorColor:param.vendorColor,sizeRange:param.sizeRange,status:param.status)
    MERGE (p) <- [:BELONGS] - (s)
    ''',parameters=batch)
