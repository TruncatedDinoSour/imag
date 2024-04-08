#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""the imag image board"""

import secrets
import typing as t
from os import makedirs

import flask
from werkzeug.middleware.proxy_fix import ProxyFix

from . import const

__version__: str = "1.0.0"


def create_app(db: str = "sqlite:///imag.db") -> t.Tuple[flask.Flask, t.Optional[str]]:
    """creates an imag app, returns a tuple of the app and the admin key if it was created"""

    app: flask.Flask = flask.Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)  # type: ignore

    app.config["SQLALCHEMY_DATABASE_URI"] = db
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["PREFERRED_URL_SCHEME"] = "https"

    app.config["SECRET_KEY"] = secrets.SystemRandom().randbytes(1024 * 16)

    from . import models

    models.limiter.init_app(app)
    models.db.init_app(app)

    admin_key: t.Optional[str] = None

    with app.app_context():
        models.db.create_all()

        if models.AccessKey.query.first() is None:
            key: models.AccessKey = models.AccessKey(models.AccessLevel.admin)
            models.db.session.add(key)
            models.db.session.commit()
            admin_key = key.key

    makedirs(const.IMAGE_DIR, exist_ok=True)

    @app.context_processor  # type: ignore
    def _() -> t.Dict[str, t.Any]:
        """expose custom stuff"""

        return {
            "desc_len": const.DESC_LEN,
            "key_len": const.KEY_LEN,
            "imagv": __version__,
        }

    @app.after_request
    def _(response: flask.Response) -> flask.Response:
        """update headers, allow all origins, hsts"""

        response.headers.extend(getattr(flask.g, "headers", {}))

        if not app.debug:
            response.headers["Content-Security-Policy"] = "upgrade-insecure-requests"
            response.headers["Strict-Transport-Security"] = (
                "max-age=63072000; includeSubDomains; preload"
            )

        response.headers["X-Frame-Options"] = "ALLOWALL"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "all"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, HEAD"

        return response

    from .api import api
    from .views import views

    app.register_blueprint(api, url_prefix="/api/")
    app.register_blueprint(views, url_prefix="/")

    return app, admin_key
