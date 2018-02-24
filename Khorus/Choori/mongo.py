import datetime
from bson import ObjectId


class Bingo:
    def __init__(self):
        self.collection = None
        self.cache = {
            'bulk': []
        }

    async def insert(self, options, payload, D, **kwargs):
        if type(D) is dict:
            D = [D]
        if '--author' in options:
            for d in D:
                d['_inserting_author'] = payload['username']
        if '--date' in options:
            now = datetime.datetime.now()
            for d in D:
                d['_inserting_date'] = now
        if '--bulk' in options:
            bulk = self.cache['bulk']
            if len(bulk) < 10:
                bulk.extend(D)
            if len(bulk) >= 10:
                result = await self.collection.insert_many(bulk)
                bulk.clear()
            else:
                return {'status': 'bulked'}
        else:
            result = await self.collection.insert_many(D)
        return [str(_id) for _id in result.inserted_ids]

    async def delete(self, options, payload, query):
        if '--query' in options:
            query[options['--query']] = payload['username']
        for key in query:  # just for primes del on enterprise
            if '_id' in key:
                try:
                    query[key] = ObjectId(query[key])
                except: pass
        return await self.collection.delete_many(query)

    async def update(self, options, payload, query, updating_json, **kwargs):
        if '--query' in options:
            query[options['--query']] = payload['username']
        if '--author' in options:
            if '$set' not in updating_json:
                updating_json['$set'] = {}
            updating_json['$set']['_updating_author'] = payload['username']
        if '--date' in options:
            if '$set' not in updating_json:
                updating_json['$set'] = {}
            updating_json['$set']['_updating_date'] = datetime.datetime.now()
        for key in query:  # just for primes del on enterprise
            if '_id' in key:
                try:
                    query[key] = ObjectId(query[key])
                except: pass
        return await self.collection.update(query, updating_json)

    async def find(self, options, payload, query, project=None, sort=None, skip=None, limit=None):
        if '--query' in options:
            query[options['--query']] = payload['username']
        for key in query:  # just for primes del on enterprise
            if '_id' in key:
                try:
                    query[key] = ObjectId(query[key])
                except: pass
        args = [query]
        if project is not None:
            args.append(project)
        documents = self.collection.find(*args)
        if skip is not None:
            documents = documents.skip(skip)
        if limit is not None:
            documents = documents.limit(limit)
        if sort is not None:
            sort = [(key, value) for key, value in sort.items()]
            documents = documents.sort(sort)
        documents = await documents.to_list(None)
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return documents

    async def aggregate(self, options, payload, aggregation):
        documents = await self.collection.aggregate(aggregation).to_list(None)
        return documents
