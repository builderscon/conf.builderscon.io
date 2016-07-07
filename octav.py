#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""OCTAV WRAPPER LIBRARY"""

import json
import requests
import os

config_file = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file, 'r') as f:
    cfg = json.load(f)['OCTAV']


class APIError(Exception):
    pass


class Octav(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=0))

    def create_user(self, nickname, auth_via, auth_user_id, **ka):
        endpoint = '/user/create'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                nickname=nickname,
                auth_via=auth_via,
                auth_user_id=auth_user_id,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def lookup_user(self, id_):
        endpoint = '/user/lookup'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def lookup_user_by_auth_id(self, auth_via, auth_user_id):
        endpoint = '/user/lookup_by_auth_user_id'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def update_user(self, id_, **ka):
        endpoint = '/user/update'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_user(self, id_):
        endpoint = '/user/delete'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def list_user(self, **ka):
        endpoint = '/user/list'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=ka
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def create_venue(self, name, address, **ka):
        endpoint = '/venue/create'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                name=name,
                address=addres,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def list_venue(self, **ka):
        endpoint = '/venue/list'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=ka
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def lookup_venue(self, id_):
        endpoint = '/venue/lookup'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def update_venue(self, id_):
        endpoint = '/vanue/update'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_venue(self, id_):
        endpoint = '/venue/delete'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def create_room(self, venue_id, name, **ka):
        endpoint = '/room/create'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                venue_id=venue_id,
                name=name,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def update_room(self, id_, **ka):
        endpoint = '/room/update'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def lookup_room(self, id_):
        endpoint = '/room/lookup'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_room(self, id_):
        endpoint = '/room/delete'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def list_room(self, venue_id, **ka):
        endpoint = '/room/list'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                venue_id=venue_id,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def create_conference(self, title, slug, user_id, **ka):
        endpoint = '/conference/create'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                title=title,
                slug=slug,
                user_id=user_id,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def add_conference_dates(self, conference_id, dates):
        endpoint = '/conference/dates/add'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                dates=dates
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_conference_dates(self, conference_id, dates):
        endpoint = '/conference/dates/delete'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                dates=dates
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def add_conference_admin(self, conference_id, user_id):
        endpoint = '/conference/admin/add'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                user_id=user_id
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_conference_admin(self, conference_id, user_id):
        endpoint = '/conference/admin/delete'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                user_id=user_id
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def add_conference_venue(self, conference_id, venue_id):
        endpoint = '/conference/venue/add'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                venue_id=venue_id
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_conference_venue(self, conference_id, venue_id):
        endpoint = '/conference/venue/delete'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                conference_id=conference_id,
                venue_id=venue_id
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def lookup_conference(self, id_):
        endpoint = '/conference/lookup'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def lookup_conference_by_slug(self, slug):
        endpoint = '/conference/lookup_by_slug'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                slug=slug
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def list_conference(self, **ka):
        endpoint = '/conference/list'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def update_conference(self, id_, **ka):
        endpoint = '/conference/update'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_conference(self, id_):
        endpoint = '/conference/delete'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def create_session(
            self, conference_id, speaker_id, title, abstract, duration, **ka
    ):
        endpoint = '/session/create'
        response = self.session.post(
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
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def lookup_session(self, id_):
        endpoint = '/session/lookup'
        response = self.session.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_session(self, id_):
        endpoint = '/session/delete'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def update_session(self, id_, **ka):
        endpoint = '/session/update'
        response = self.session.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def list_session_by_conference(self, conference_id, **ka):
        endpoint = '/schedule/list'
        response = request.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                conference_id=conference_id,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

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
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def delete_question(self, id_):
        endpoint = '/question/delete'
        response = request.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                id=id_
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def list_question(self, session_id, **ka):
        endpoint = '/question/list'
        response = request.get(
            cfg['BASE_URI'] + endpoint,
            params=dict(
                session_id=session_id,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError

    def create_session_survey_response(
            self, session_id, user_id, user_prior_knowledge, speaker_knowledge,
            speaker_presentation, material_quality, overall_rating, **ka
    ):
        endpoint = '/session/create'
        response = request.post(
            cfg['BASE_URI'] + endpoint,
            auth=(cfg['key'], cfg['secret']),
            data=dict(
                session_id=session_id,
                user_id=user_id,
                user_prior_knowledge=user_prior_knowledge,
                speaker_knowledge=speaker_knowledge,
                speaker_presentation=speaker_presentation,
                material_quality=material_quality,
                overall_rating=overall_rating,
                **ka
            )
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError
