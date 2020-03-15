from werkzeug.wrappers import Response
from db_utils import *

import json
import traceback


def get_actor_response(_id):
    result = get_actor_by_id(_id)

    if result:
        response = Response(
            json.dumps(result, indent=4, default=str),
            mimetype='application/json',
            status=200
        )

        return response

    else:
        response = Response(
            json.dumps(
                {
                    "error": "{} couldn't be found in database, check again later.".format(_id),
                    "status": 404
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=404
        )

        return response


def update_actor_response(_id, data):
    try:
        result = update_actor(_id, data)

    except:
        print(traceback.format_exc())
        response = Response(
            json.dumps(
                {
                    'status': 500,
                    'message': "Internal server error for {}".format(_id)
                },
                indent=4,
                default=str
            )
        )

        return response

    if result:
        response = Response(
            json.dumps(
                {
                    'status': 200,
                    'message': "PUT operation has been successful for {}".format(_id)
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=200
        )

        return response

    else:
        response = Response(
            json.dumps(
                {
                    'status': 404,
                    'message': 'Couldn\'t find ObjectId({})'.format(_id)
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=404
        )

        return response


def delete_actor_response(_id):
    result = delete_actor(_id)

    if result:
        response = Response(
            json.dumps(
                {
                    'status': 200,
                    'message': 'DELETE operation has been successful for {}'.format(_id)
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=200
        )

        return response

    else:
        response = Response(
            json.dumps(
                {
                    'status': 404,
                    'message': 'Couldn\'t find ObjectId({})'.format(_id)
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=404
        )

        return response


def insert_actor_response(data):
    try:
        data = json.loads(data)

    except json.decoder.JSONDecodeError:
        response = Response(
            json.dumps(
                {
                    'status': 400,
                    'message': "Bad JSON Request"
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=400
        )

        return response

    result, err = insert_actor(data)

    if result:
        response = Response(
            json.dumps(
                {
                    'status': 200,
                    'message': 'Actor added successfully'
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=200
        )

        return response

    else:
        response = Response(
            json.dumps(
                {
                    'status': 409,
                    'message': err
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=409
        )

        return response


def replace_actors_collection(data):
    try:
        data = json.loads(data)

    except json.decoder.JSONDecodeError:
        response = Response(
            json.dumps(
                {
                    'status': 400,
                    'message': "Bad JSON Request"
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=400
        )

        return response

    count = update_collection(data)
    if count == 0:
        response = Response(
            json.dumps(
                {
                    'status': 200,
                    'message': 'No new actors have been added (Database has been deleted)'
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=200
        )

        return response

    else:
        response = Response(
            json.dumps(
                {
                    'status': 200,
                    'message': 'Collection \'actors\' has been successfully updated (Added {} new entries to collection)'
                        .format(count)
                },
                indent=4,
                default=str
            ),
            mimetype='application/json',
            status=200
        )

        return response


def get_actors_collection():
    result = get_actors()
    response = Response(
        json.dumps(result, default=str, indent=4),
        mimetype='application/json',
        status=200
    )

    return response


def delete_actors_collection():
    result = delete_actors()
    response = Response(
        json.dumps(
            {
                'status': 200,
                'message': "Deleted {} entries successfully".format(result)
            },
            default=str,
            indent=4
        ),
        mimetype='application/json',
        status=200
    )

    return response
