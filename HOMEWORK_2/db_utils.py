from bson.objectid import ObjectId
from pymongo import MongoClient

server = MongoClient('127.0.0.1', 27017)
database = server['database']
actors = database['actors']


def get_actor_by_id(_id):
    return actors.find_one({'_id': ObjectId(_id)})


def get_actor_by_name(name):
    return actors.find_one({'name': name})


def delete_actor(_id):
    return actors.delete_one({"_id": ObjectId(_id)})


def update_actor(_id, data):
    new_object = get_actor_by_id(_id)

    if 'name' in data:
        new_object['name'] = data['name']
    if 'age' in data:
        new_object['age'] = data['age']
    if 'born' in data:
        new_object['born'] = data['born']
    if 'movies' in data:
        new_object['movies'] = data['movies']

    return actors.replace_one({'_id': ObjectId(_id)}, new_object, upsert=False), ''


def insert_actor(data):
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
    if result:
        return None, 'Entry \'{}\' exists already'.format(data['name'])

    return actors.insert_one(data), ''


def update_collection(data):
    count = 0
    if not isinstance(data, list):
        return None, 'Please provide a list of actors'

    delete_actors()
    for actor in data:
        result = get_actor_by_name(actor['name'])
        if not result:
            actors.insert_one(actor)
            count += 1

    return count


def get_actors():
    actors_cursor = actors.find({'_id': {'$gt': ObjectId('0' * 24)}})
    result = list()

    for actor in actors_cursor:
        result.append(actor)

    return result


def delete_actors():
    delete_object = actors.delete_many({'_id': {'$gt': ObjectId('0' * 24)}})
    return delete_object.deleted_count
