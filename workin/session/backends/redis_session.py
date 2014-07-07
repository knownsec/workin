#!/usr/bin/python
# coding: utf-8

import uuid
import hmac
import json
import hashlib
import redis
import logging

from workin.session import SessionData, InvalidSessionException


class RedisSessionEngine(object):
    def __init__(self, secret, store_options, session_timeout):
        self.secret = secret
        self.session_timeout = session_timeout
        try:
            if store_options.get('redis_pass'):
                self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'], password=store_options['redis_pass'])
            else:
                self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'])
        except Exception, e:
            logging.exception("RedisSessionEngine init failed: %s" % e)

    def _fetch(self, session_id):
        try:
            session_data = raw_data = self.redis.get(session_id)
            if raw_data is not None:
                self.redis.setex(session_id, self.session_timeout, raw_data)
                session_data = json.loads(raw_data)

            if isinstance(session_data, dict):
                return session_data
            else:
                return {}
        except IOError:
            return {}

    def get(self, request_handler=None):
        if (request_handler is None):
            session_id = None
            hmac_key = None
        else:
            session_id = request_handler.get_secure_cookie("session_id")
            hmac_key = request_handler.get_secure_cookie("verification")

        if session_id is None:
            session_exists = False
            session_id = self._generate_id()
            hmac_key = self._generate_hmac(session_id)
        else:
            session_exists = True
        check_hmac = self._generate_hmac(session_id)
        if hmac_key != check_hmac:
            raise InvalidSessionException()

        session = SessionData(session_id, hmac_key)

        if session_exists:
            session_data = self._fetch(session_id)
            for key, data in session_data.iteritems():
                session[key] = data
        return session

    def set(self, request_handler, session):
        request_handler.set_secure_cookie("session_id", session.session_id)
        request_handler.set_secure_cookie("verification", session.hmac_key)

        session_data = json.dumps(dict(session.items()))

        self.redis.setex(session.session_id, self.session_timeout, session_data)

    def _generate_id(self):
        new_id = hashlib.sha256(self.secret + str(uuid.uuid4()))
        return new_id.hexdigest()

    def _generate_hmac(self, session_id):
        return hmac.new(session_id, self.secret, hashlib.sha256).hexdigest()
