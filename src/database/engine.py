import motor.motor_asyncio


class DataBase:
    def __init__(self, connection_url: str, db_name: str, collection_name: str):
        self.collection = motor.motor_asyncio.AsyncIOMotorClient(connection_url)[db_name][collection_name]

    async def add(self, data: dict, multiple: bool = False):
        if multiple is True:
            return await self.collection.insert_many(data).inserted_ids
        else:
            return await self.collection.insert_one(data).inserted_id

    async def find(self, data: dict, multiple: bool = False, sort: [str, list] = None):
        if multiple is True:
            cursor = self.collection.find(data)

            if sort is not None:
                cursor = cursor.sort(sort)

            return [document for document in await cursor.to_list(int(1e10))]

        else:
            return await self.collection.find_one(data)

    async def delete(self, data: dict, multiple: bool = False):
        if multiple is True:
            return await self.collection.delete_many(data).deleted_count
        else:
            return await self.collection.delete_one(data).deleted_count

    async def update(self, old_data: dict, new_data: dict, multiple: bool = False):
        if multiple is True:
            return await self.collection.update_many(
                old_data, {"$set": new_data}
            ).modified_count
        else:
            return await self.collection.update_one(
                old_data, {"$set": new_data}
            ).modified_count
