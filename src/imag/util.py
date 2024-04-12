#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""utilities"""

import typing as t
from functools import wraps

import flask

from .models import AccessKey, AccessLevel


def require_args(
    *form_args: str,
) -> t.Callable[[t.Callable[..., t.Any]], t.Callable[..., t.Any]]:
    """require form arguments"""

    def wrapper(fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
        @wraps(fn)
        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            for arg in form_args:
                if arg not in flask.request.form.keys():
                    flask.abort(400)

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def with_access(
    access_level: AccessLevel,
) -> t.Callable[[t.Callable[..., t.Any]], t.Callable[..., t.Any]]:
    """force access level"""

    def wrapper(fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
        @wraps(fn)
        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            if "key" not in flask.request.form:
                flask.abort(400)

            access: t.Optional[AccessKey] = AccessKey.query.filter_by(  # type: ignore
                key=flask.request.form.get("key")
            ).first()

            flask.g.setdefault("access", access.access_level)  # type: ignore

            if access and (access.access_level.value >= access_level.value):  # type: ignore
                return fn(*args, **kwargs)  # type: ignore
            else:
                flask.abort(403)

        return decorator

    return wrapper


def make_api(
    response: flask.Response,
    cors: bool = True,
    cache: bool = False,
) -> flask.Response:
    """make api endpoint ( disables cors and caching )"""

    if cors:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

    if not cache:
        response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
        response.headers["Cache-Control"] = (
            "max-age=0, no-cache, must-revalidate, proxy-revalidate"
        )

    return response


def api(fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
    """api endpoint"""

    @wraps(fn)
    def wrapper(*args: t.Any, **kwargs: t.Any) -> flask.Response:
        """decorator"""
        return make_api(
            flask.make_response(fn(*args, **kwargs)),
            cache=True,
        )

    return wrapper
