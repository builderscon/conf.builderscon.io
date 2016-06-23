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

    def update_user(self, id_, **ka):
        endpoint = '/user/update'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_,
                **ka
            )
        )
        return response

    def delete_user(self, id_):
        endpoint = '/user/delete'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        return response

    def list_user(self, **ka):
        endpoint = '/user/list'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=ka
        )
        return response

    def create_venue(self, name, address, **ka):
        endpoint = '/venue/create'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                name=name,
                address=addres,
                **ka
            )
        )
        return response

    def list_venue(self, **ka):
        endpoint = '/venue/list'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=ka
        )
        return response

    def lookup_venue(self, id_):
        endpoint = '/venue/lookup'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        return response

    def update_venue(self, id_):
        endpoint = '/vanue/update'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        return response

    def delete_venue(self, id_):
        endpoint = '/venue/delete'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        return response

    def create_room(self, venue_id, name, **ka):
        endpoint = '/room/create'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                venue_id=venue_id,
                name=name,
                **ka
            )
        )
        return response

    def update_room(self, id_, **ka):
        endpoint = '/room/update'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_,
                **ka
            )
        )
        return response

    def lookup_room(self, id_):
        endpoint = '/room/lookup'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        return response

    def delete_room(self, id_):
        endpoint = '/room/delete'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        return response

    def list_room(self, venue_id, **ka):
        endpoint = '/room/list'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                venue_id=venue_id,
                **ka
            )
        )
        return response

    def create_conference(self, title, slug, user_id, **ka):
        endpoint = '/conference/create'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                title=title,
                slug=slug,
                user_id=user_id,
                **ka
            )
        )
        return response

    def add_conference_dates(self, conference_id, dates):
        endpoint = '/conference/dates/add'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                dates=dates
            )
        )
        return response

    def delete_conference_dates(self, conference_id, dates):
        endpoint = '/conference/dates/delete'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                dates=dates
            )
        )
        return response

    def add_conference_admin(self, conference_id, user_id):
        endpoint = '/conference/admin/add'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                user_id=user_id
            )
        )
        return response

    def delete_conference_admin(self, conference_id, user_id):
        endpoint = '/conference/admin/delete'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                user_id=user_id
            )
        )
        return response

    def add_conference_venue(self, conference_id, venue_id):
        endpoint = '/conference/venue/add'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                venue_id=venue_id
            )
        )
        return response

    def delete_conference_venue(self, conference_id, venue_id):
        endpoint = '/conference/venue/delete'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                venue_id=venue_id
            )
        )
        return response

    def lookup_conference(self, id_):
        endpoint = '/conference/lookup'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        return response

    def lookup_conference_by_slug(self, slug):
        endpoint = '/conference/lookup_by_slug'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                slug=slug
            )
        )
        return response

    def list_conference(self, **ka):
        endpoint = '/conference/list'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                **ka
            )
        )
        return response

    def update_conference(self, id_, **ka):
        endpoint = '/conference/update'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_,
                **ka
            )
        )
        return response

    def delete_conference(self, id_):
        endpoint = '/conference/delete'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        return response

    def create_session(
            self, conference_id, speaker_id, title, abstract, duration, **ka
    ):
        endpoint = '/session/create'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                speaker_id=speaker_id,
                title=title,
                abstract=abstract,
                duration=duration,
                **ka
            )
        )
        return response

    def lookup_session(self, id_):
        endpoint = '/session/lookup'
        response = requests.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        return response

    def delete_session(self, id_):
        endpoint = '/session/delete'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        return response

    def update_session(self, id_, **ka):
        endpoint = '/session/update'
        response = requests.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_,
                **ka
            )
        )
        return response

    def list_session_by_conference(self, conference_id, **ka):
        endpoint = '/schedule/list'
        response = request.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                conference_id=conference_id,
                **ka
            )
        )
        return response

    def create_question(self, session_id, user_id, body):
        endpoint = '/question/create'
        response = request.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                session_id=sessoin_id,
                user_id=user_id,
                body=body
            )
        )
        return response

    def delete_question(self):
        pass

    def list_question(self):
        pass

    def create_session_survey_response(self):
        pass
