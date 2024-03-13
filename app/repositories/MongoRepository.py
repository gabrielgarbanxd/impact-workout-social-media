import math
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson.objectid import ObjectId
from datetime import datetime
from config import Config

class MongoRepository:
    def __init__(self, collection_name):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DBNAME]
        self.collection = self.db[collection_name]

    def __add_updated_at(self, data):
        data['updated_at'] = datetime.now()
        return data
    
    def __add_created_at(self, data):
        data['created_at'] = datetime.now()
        return data

    def paginate(self, query={}, projection={}, page=1, per_page=25, sort=None, descendind=True):
        total_docs = self.count(query)
        total_pages = math.ceil(total_docs / per_page)

        direction = DESCENDING if descendind else ASCENDING

        if sort is not None:
            cursor = self.collection.find(query, projection).sort(sort, direction).skip((page - 1) * per_page).limit(per_page)
        else:
            cursor = self.collection.find(query, projection).skip((page - 1) * per_page).limit(per_page)

        paginated_data = {
            "total_pages": total_pages,
            "total_documents": total_docs,
            "current_page": page,
            "per_page": per_page,
            "data": list(cursor)
        }
        return paginated_data


    def count(self, query = {}):
        return self.collection.count_documents(query)

    def aggregate(self, pipeline):
        return self.collection.aggregate(pipeline)


    # =========>> GET ALL METHODS <<=========
    def get_all(self, paginated = False, page = 1, per_page=25, sort = None, descendind=True):
        if paginated:
            return self.paginate(page=page, per_page=per_page, sort=sort)
        
        direction = DESCENDING if descendind else ASCENDING

        if sort is not None:
            return self.collection.find().sort(sort, direction)

        return self.collection.find()
    
    def get_all_with_projection(self, projection, paginated = False, page = 1, per_page=25, sort = None):
        if paginated:
            return self.paginate(projection=projection, page=page, per_page=per_page, sort=sort)
        
        if sort is not None:
            return self.collection.find({}, projection).sort(sort, DESCENDING)

        return self.collection.find({}, projection)
    
    def get_by(self, field, value, paginated = False, page = 1, per_page=25, sort = None):
        if paginated:
            return self.paginate(query={field: value}, page=page, per_page=per_page, sort=sort)
        
        if sort is not None:
            return self.collection.find({field: value}).sort(sort, DESCENDING)
        
        return self.collection.find({field: value})
    
    def get_by_with_projection(self, field, value, projection, paginated = False, page = 1, per_page=25, sort = None):
        if paginated:
            return self.paginate(query={field: value}, projection=projection, page=page, per_page=per_page, sort=sort)
        
        if sort is not None:
            return self.collection.find({field: value}, projection).sort(sort, DESCENDING)
        
        return self.collection.find({field: value}, projection)
    
    def get_by_query(self, query, paginated = False, page = 1, per_page=25, sort = None):
        if paginated:
            return self.paginate(query=query, page=page, per_page=per_page, sort=sort)
        
        if sort is not None:
            return self.collection.find(query).sort(sort, DESCENDING)
        
        return self.collection.find(query)
    
    def get_by_query_with_projection(self, query, projection, paginated = False, page = 1, per_page=25, sort = None, descendind=True):
        if paginated:
            return self.paginate(query=query, projection=projection, page=page, per_page=per_page, sort=sort, descendind=descendind)
        
        if sort is not None:
            return self.collection.find(query, projection).sort(sort, DESCENDING)
        
        return self.collection.find(query, projection)
    
    def get_by_fk(self, field, value, paginated = False, page = 1, per_page=25, sort = None):
        if paginated:
            return self.paginate(query={field: ObjectId(value)}, page=page, per_page=per_page, sort=sort)
        
        if sort is not None:
            return self.collection.find({field: ObjectId(value)}).sort(sort, DESCENDING)
        
        return self.collection.find({field: ObjectId(value)})

    def get_by_fk_with_projection(self, field, value, projection, paginated = False, page = 1, per_page=25, sort = None, descendind=True):
        if paginated:
            return self.paginate(query={field: ObjectId(value)}, projection=projection, page=page, per_page=per_page, sort=sort, descendind=descendind)
        
        if sort is not None:
            return self.collection.find({field: ObjectId(value)}, projection).sort(sort, DESCENDING)
        
        return self.collection.find({field: ObjectId(value)}, projection)


    # =========>> GET ONE METHODS <<=========
    def get_one(self, id):
        return self.collection.find_one({'_id': ObjectId(id)})
    
    def get_one_by_query(self, query):
        return self.collection.find_one(query)
    
    def get_one_with_projection(self, id, projection):
        return self.collection.find_one({'_id': ObjectId(id)}, projection)

    def get_one_by(self, field, value):
        return self.collection.find_one({field: value})


    # =========>> INSERT METHODS <<=========
    def insert(self, data):
        data_with_created_at = self.__add_created_at(data)
        return self.collection.insert_one(data_with_created_at)
    
    def insert_many(self, data):
        data_with_created_at = list(map(self.__add_created_at, data))
        return self.collection.insert_many(data_with_created_at)


    # =========>> UPDATE METHODS <<=========
    def update(self, id, data):
        data_with_updated_at = self.__add_updated_at(data)
        return self.collection.update_one({'_id': ObjectId(id)}, {'$set': data_with_updated_at})


    # =========>> DELETE METHODS <<=========
    def delete(self, id):
        return self.collection.delete_one({'_id': ObjectId(id)})
    
    def delete_by(self, field, value):
        return self.collection.delete_one({field: value})

    def delete_all(self):
        return self.collection.delete_many({})