import pymongo


class DataBase:
    def __init__(self, connection_url, db_name, collection_name):
        self.collection = pymongo.MongoClient(connection_url)[db_name][collection_name]

    def add(self, data: dict, multiple: bool = False):
        if multiple is True:
            return self.collection.insert_many(data).inserted_ids
        else:
            return self.collection.insert_one(data).inserted_id

    def find(self, data: dict, multiple: bool = False, sort: [str, list] = None):
        if multiple is True:
            if sort is None:
                return [x for x in self.collection.find(data)]
            else:
                return [x for x in self.collection.find(data).sort(sort)]
        else:
            return self.collection.find_one(data)

    def delete(self, data: dict, multiple: bool = False):
        if multiple is True:
            return self.collection.delete_many(data).deleted_count
        else:
            return self.collection.delete_one(data).deleted_count

    def update(self, old_data: dict, new_data: dict, multiple: bool = False):
        if multiple is True:
            return self.collection.update_many(old_data, {"$set": new_data}).modified_count
        else:
            return self.collection.update_one(old_data, {"$set": new_data}).modified_count
