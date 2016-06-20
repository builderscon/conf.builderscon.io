#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import MySQLdb

with open('conf.json', 'r') as f:
    cfg = json.load(f)

with MySQLdb.connect(**cfg['DB_INFO']) as cursor:
    cursor.execute(
        '''CREATE TABLE auth_sessions (
        username VARCHAR(128) NOT NULL,
        session_id VARCHAR(64) NOT NULL,
        expire DATETIME NOT NULL
        );
        '''
    )
