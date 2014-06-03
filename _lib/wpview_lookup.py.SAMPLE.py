import json

import flask
import requests


class WPView(object):
    def __init__(self, data):
        self.data = data

    @property
    def hero(self):
        hero_id = self.data['post']['custom_fields']['related_hero'][0]
        hero_url = "http://your.wordpress.domain/api/get_post/?post_id=" + hero_id + "&post_type=cfpb_hero"
        response = requests.get(hero_url)
        hero_data = json.loads(response.text)
        return hero_data['post']

def do_lookup():
    request = flask.request    
    json_url = "http://your.wordpress.domain/view" + request.path + "?json=1"
    response = requests.get(json_url)
    data = json.loads(response.text)
    return WPView(data)
