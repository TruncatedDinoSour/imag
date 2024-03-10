#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""app routing helper"""

from typing import Any

from flask import Blueprint, Response

from .util import make_api


class Bp(Blueprint):
    def get(self, rule: str, **kwargs: Any) -> Any:
        """wrapper for GET"""
        return self.route(rule=rule, methods=("GET",), **kwargs)

    def post(self, rule: str, **kwargs: Any) -> Any:
        """wrapper for POST"""
        return self.route(rule=rule, methods=("POST",), **kwargs)

    def set_api(self) -> "Bp":
        """disable cors and cache"""

        @self.after_request  # type: ignore
        def _(response: Response) -> Response:
            """disable cache"""
            return make_api(response)

        return self
