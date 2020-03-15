from werkzeug.wrappers import Response
from db_utils import *

import json
import traceback


def get_actor_response(_id):
    result, err = get_actor_by_id(_id)

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
    result, err = delete_actor(_id)

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


def insert_user_response(data):
    data = json.loads(data)
    result, err = insert_user(data)

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
