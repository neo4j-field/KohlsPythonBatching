



def create_product_and_sku(tx,batch):
    tx.run(
    '''
    UNWIND $batch as param
    MERGE (p:Product {title:param.title,variation:param.variation,altTag:param.altTag,description:param.description,brand:param.brand})
    WITH param,p
    MERGE (s:SKU {id:param.id,colorFamily:param.colorFamily,displayColor:param.displayColor,vendorColor:param.vendorColor,sizeRange:param.sizeRange,status:param.status)
    MERGE (p) <- [:BELONGS] - (s)
    ''',parameters=batch)





def create_product(tx,batch):
    tx.run(
    '''
    UNWIND $batch as param
    MERGE (p:Product {title:param.title})
    SET p.variations=param.variations,p.altTag=param.altTag,p.description=param.description,p.brand=param.brand
    '''
    ,parameters=batch)



def create_sku(tx,batch):
    result = tx.run(
    '''
    UNWIND $batch as param
    MERGE (s:SKU {id:param.id}) 
    SET s.colorFamily=param.colorFamily,s.displayColor=param.displayColor,s.vendorColor=param.vendorColor,s.sizeRange=param.sizeRange,s.status=param.status
    ''',
        parameters = batch
    )

    result.single()
    return result.consume()



