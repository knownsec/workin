#!/usr/bin/env python
# coding: utf-8


def auth(handler):
    if not handler.application.session_engine:
        return {}

    return {'user': handler.get_current_user()}
