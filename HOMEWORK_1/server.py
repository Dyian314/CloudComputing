import time
import logging

from server_utils import *
from flask import Flask, jsonify, render_template, g, request
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    diff = round(time.time() - g.start, 4)
    url = "/" + "/".join(request.url.split("/")[3:])

    update_metrics(url, response.status_code)
    app.logger.debug("{} is making a {} to {}. Latency: {}, status code {}".format(request.remote_addr,
                                                                                   request.method,
                                                                                   url,
                                                                                   diff,
                                                                                   response.status))
    return response


@app.route("/", methods=['GET'])
def index():
    return render_template('home.html'), 200


@app.route("/weather", methods=['GET'])
def get_weather():
    client_address, err = get_ip_address()
    days = int(request.args.get('days', 1))
    if days < 0:
        days *= -1

    if days > 14:
        days = 14

    if client_address is None:
        app.logger.error("Error because {}".format(err))
        return render_template('weather.html',
                               error="Couldn't get IP address because --> {}".format(err))

    app.logger.info(client_address)
    info, err = get_info(client_address)
    if info is None:
        app.logger.error(err)
        return render_template('weather.html',
                               error="Couldn't get info about IP {} because --> {}".format(client_address, err))

    api_key = os.getenv("WEATHER_API_KEY")
    url = "http://api.worldweatheronline.com/premium/v1/weather.ashx?key={}&q={},{}&format=json&num_of_days={}".\
        format(api_key, info['latitude'], info['longitude'], days)

    response = requests.request("GET", url)
    app.logger.debug(response.content)
    if response.status_code is 200:
        weather_info = json.loads(response.content)
        data = weather_info['data']['current_condition'][0]

        weather = get_weather_data(weather_info)
        app.logger.info(weather_info)

        update_metrics("http://api.worldweatheronline.com/premium/v1/weather.ashx", response.status_code)
        return render_template('weather.html',
                               address=client_address,
                               country=info['country_name'],
                               city_name=info['city'],
                               coords=(info['latitude'], info['longitude']),
                               country_flag=info['location']['country_flag'],
                               time=data['observation_time'],
                               weather=weather)

    update_metrics("http://api.worldweatheronline.com/premium/v1/weather.ashx", response.status_code)
    return render_template('weather.html',
                           error="Couldn't reach Weather API (status code: {})".format(response.status_code))


@app.route("/metrics", methods=['GET'])
def get_metrics():
    return jsonify(metrics)


if __name__ == '__main__':
    formatter = logging.Formatter("%(asctime)-15s | %(name)s | %(levelname)s | %(message)-30s")
    handler = RotatingFileHandler('server.log', maxBytes=100000, backupCount=1)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.run()
