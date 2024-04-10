#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""the API for imag"""

import typing as t

import flask
from werkzeug.wrappers import Response

from . import models, util
from .routing import Bp

api: Bp = Bp("api", __name__).set_api()


@api.get("/latest")
def latest_image() -> flask.Response:
    """get latest image id"""
    return flask.Response(str(models.Image.query.order_by((models.Image.created).desc()).first().iid), 200, content_type="text/plain")  # type: ignore


@api.get("/all")
def all_mages() -> flask.Response:
    """get latest image id"""
    return flask.jsonify(
        [
            img.json()  # type: ignore
            for img in models.Image.query.order_by((models.Image.created if "newest" == flask.request.args.get("s") else models.Image.score).desc()).all()  # type: ignore
        ]
    )


@api.get("/image/<int:iid>")
def image(iid: int) -> flask.Response:
    """get image data"""
    return flask.jsonify(models.Image.query.filter_by(iid=iid).first_or_404().json())


@api.get("/search")
def search() -> flask.Response:
    """get image data"""

    query: t.Optional[str] = flask.request.args.get("q")

    if not query:
        flask.abort(400)

    return flask.jsonify([image.json() for image in models.Image.by_search(query, flask.request.args.get("s") != "newest")])  # type: ignore


@api.post("/key")
@util.with_access(models.AccessLevel.admin)
def key() -> str:
    """only admins can access this"""
    return "Congrats! You can access the admin-only key api."


@api.post("/key/new")
@util.with_access(models.AccessLevel.admin)
@util.require_args("perm")
def new_key() -> str:
    """generate a new key"""

    try:
        access: models.AccessLevel = models.AccessLevel[flask.request.form["perm"]]
    except KeyError:
        flask.abort(400)

    key: models.AccessKey = models.AccessKey(access)

    models.db.session.add(key)
    models.db.session.commit()

    return key.key


@api.post("/key/revoke")
@util.with_access(models.AccessLevel.admin)
@util.require_args("rev")
def revoke_key() -> str:
    """revoke an access key"""

    key: models.AccessKey = models.AccessKey.query.filter_by(
        key=flask.request.form["rev"]
    ).first_or_404()

    models.db.session.delete(key)
    models.db.session.commit()

    return key.key


@api.post("/key/keys")
@util.with_access(models.AccessLevel.admin)
def list_keys() -> Response:
    """show all access keys"""
    return flask.jsonify([key.json() for key in models.AccessKey.query.all()])  # type: ignore


@api.post("/key/info")
@util.with_access(models.AccessLevel.admin)
@util.require_args("target")
def key_info() -> Response:
    """show info about a key"""
    return flask.jsonify(models.AccessKey.query.filter_by(key=flask.request.form["target"]).first_or_404().json())  # type: ignore
