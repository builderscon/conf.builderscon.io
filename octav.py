#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""OCTAV WRAPPER LIBRARY"""

import json
import requests
import os

config_file = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file, 'r') as f:
    cfg = json.load(f)['OCTAV']


class Octav(object):
    def __init__(self):
        pass

    def create_user(self, nickname, auth_via, auth_user_id, **ka):
        endpoint = '/user/create'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                nickname=nickname,
                auth_via=auth_via,
                auth_user_id=auth_user_id,
                **ka
            )
        )
        return response


    def lookup_user(self, id_):
        endpoint = '/user/lookup'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        return response

    def lookup_user_by_auth_id(self, auth_via, auth_user_id):
        endpoint = '/user/lookup_by_auth_user_id'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
            )
        )
        return response

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def list_user(self):
        pass

    def create_venue(self):
        pass

    def list_venue(self):
        pass

    def lookup_venue(self):
        pass

    def update_venue(self):
        pass

    def delete_venue(self):
        pass

    def create_room(self):
        pass

    def update_room(self):
        pass

    def lookup_room(self):
        pass

    def delete_room(self):
        pass

    def list_room(self):
        pass

    def create_conference(self):
        pass

    def add_conference_dates(self):
        pass

    def delete_conference_dates(self):
        pass

    def add_conference_admin(self):
        pass

    def delete_conference_admin(self):
        pass

    def add_conference_venue(self):
        pass

    def delete_conference_venue(self):
        pass

    def lookup_conference(self):
        pass

    def lookup_conference_by_slug(self):
        pass

    def list_conference(self):
        pass

    def update_conference(self):
        pass

    def delete_conference(self):
        pass

    def create_session(self):
        pass

    def lookup_session(self):
        pass

    def delete_session(self):
        pass

    def update_session(self):
        pass

    def list_session_by_conference(self):
        pass

    def create_question(self):
        pass

    def delete_question(self):
        pass

    def list_question(self):
        pass

    def create_session_survey_response(self):
        pass
