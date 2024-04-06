#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""views"""

import os
import typing as t
from datetime import datetime

import flask
import magic
from werkzeug.wrappers import Response

from . import const, models, util
from .routing import Bp

views: Bp = Bp("views", __name__)


@views.get("/")
def index() -> str:
    """index page"""
    return flask.render_template(
        "index.j2",
        images=models.Image.query.order_by(models.Image.created.desc()).all(),  # type: ignore
    )


@views.post("/")
@util.with_access(models.AccessLevel.write)
def post_image() -> Response:
    """post image"""

    if "image" not in flask.request.files:
        flask.abort(400)

    file: t.Any = flask.request.files["image"]

    mime: t.Any = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)  # reset file pointer to start of file

    if not mime.startswith("image/"):
        flask.abort(400, "Invalid image file.")

    image: models.Image = models.Image((flask.request.form.get("desc") or "").strip())

    models.db.session.add(image)
    models.db.session.commit()

    file.save(os.path.join(const.IMAGE_DIR, str(image.iid)))

    return flask.redirect(flask.url_for("views.image", iid=image.iid))


@views.get("/search")
def search() -> t.Union[Response, str]:
    """search images based on the query"""

    query: t.Optional[str] = flask.request.args.get("q")

    if not query:
        return flask.redirect("/")

    return flask.render_template(
        "index.j2",
        images=models.Image.by_search(query),  # type: ignore
        title=query,
        q=query,
    )


@views.get("/image/<int:iid>.jpg")
@views.get("/image/<int:iid>.png")
@views.get("/image/<int:iid>")
@util.api
def image(iid: int) -> flask.Response:
    """get image"""

    try:
        with open(os.path.join(const.IMAGE_DIR, str(iid)), "rb") as fp:
            file: bytes = fp.read()
            return flask.Response(file, mimetype=magic.from_buffer(file, mime=True))  # type: ignore
    except FileNotFoundError:
        flask.abort(404)


@views.post("/edit/<int:iid>")
@util.with_access(models.AccessLevel.write)
def edit(iid: int) -> Response:
    """edit image ( details )"""

    image: models.Image = models.Image.query.filter_by(iid=iid).first_or_404()

    if flask.request.form.get("delete"):
        models.db.session.delete(image)
        models.db.session.commit()
        flask.flash(f"Image {image.iid} deleted.")
        return flask.redirect("/")

    if (desc := flask.request.form.get("desc")) is not None:
        image.desc = desc
        flask.flash("Image description edited.")

    if "image" in flask.request.files:
        file: t.Any = flask.request.files["image"]

        mime: t.Any = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)

        if mime.startswith("image/"):
            file.save(os.path.join(const.IMAGE_DIR, str(image.iid)))
            flask.flash("Image file edited.")

    image.edited = datetime.utcnow()  # type: ignore
    models.db.session.commit()

    return flask.redirect("/")
