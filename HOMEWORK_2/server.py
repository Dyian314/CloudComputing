from __future__ import print_function

from handle_requests import *
from gevent.pywsgi import WSGIServer
from werkzeug.wrappers import Response, Request

import re
import json


def handle_collection_actors(request):
    method = request.method

    if method == 'POST':
        data = request.data  # Adds items
        response = insert_actor_response(data)
        return response

    elif method == 'PUT':  # Replaces collection
        data = request.data
        response = replace_actors_collection(data)
        return response

    elif method == 'GET':
        response = get_actors_collection()
        return response

    elif method == 'DELETE':
        response = delete_actors_collection()
        return response


def handle_unique_actor(request):
    allowed_methods = ['GET', 'PUT', 'DELETE']

    method = request.method
    mongo_id = request.url.split("/")[-1]

    if method not in allowed_methods:
        response = Response(
            json.dumps({"status": 405, "message": "Method not allowed"}, indent=4, default=str),
            status=405
        )
        response.headers['Allow'] = 'GET, PUT, DELETE'

        return response

    if method == 'GET':
        response = get_actor_response(mongo_id)
        return response

    elif method == 'PUT':
        data = json.loads(request.data)
        response = update_actor_response(mongo_id, data)
        return response

    elif method == 'DELETE':
        response = delete_actor_response(mongo_id)
        return response


def hello_world(request):
    if request.method == 'GET':
        response = Response(
            "Hello world!",
            mimetype='application/json',
            status=200
        )

        return response

    else:
        response = Response(
            headers='Allow: GET',
            status=405
        )

        return response


def application(env, start_response):
    request = Request(env)
    path = env['PATH_INFO'] or '/'
    for valid_path in paths:
        if re.search(valid_path, path):
            response = paths[valid_path](request)
            if response:
                return response(env, start_response)

    else:
        response = Response(
            json.dumps({"status": 404, "message": "Couldn't find page :("}, indent=4, default=str),
            status=404
        )

        return response(env, start_response)


paths = {
    '^/api/v1/actors$': handle_collection_actors,
    '^/api/v1/actors/[a-zA-Z0-9]{24}$': handle_unique_actor,
    '^/$': hello_world
}

if __name__ == '__main__':
    port = 5000
    print('Serving on {}..'.format(port))
    WSGIServer(('0.0.0.0', port), application).serve_forever()
