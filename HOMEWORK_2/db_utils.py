from bson.objectid import ObjectId
from pymongo import MongoClient

server = MongoClient('127.0.0.1', 27017)
database = server['database']
actors = database['actors']


def get_actor_by_id(_id):
    return actors.find_one({'_id': ObjectId(_id)})


def get_actor_by_name(name):
    return None


def delete_actor(_id):
    return actors.delete_one({"_id": ObjectId(_id)})


def update_actor(_id, data):
    new_object, err = get_actor_by_id(_id)

    if 'name' in data:
        new_object['name'] = data['name']
    if 'age' in data:
        new_object['age'] = data['age']
    if 'born' in data:
        new_object['born'] = data['born']
    if 'movies' in data:
        new_object['movies'] = data['movies']

    return actors.replace_one({'_id': ObjectId(_id)}, new_object, upsert=False), ''


def insert_user(data):
    if 'name' not in data:
        return None, "'name' is not present in the request"
    if 'age' not in data:
        return None, "'age' is not present in the request"
    if 'born' not in data:
        return None, "'born' is not present in the request"
    if 'movies' not in data:
        return None, "'movies' is not present in the request"
    elif not isinstance(data["movies"], list):
        return None, "Invalid 'movies' type -- should be list"

    result = get_actor_by_name(data['name'])
    if not result:
        return None, 'Entry \'{}\' exists already'.format(data['name'])

    return actors.insert_one(data), ''
