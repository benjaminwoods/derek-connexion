import os
from pathlib import Path

from flask import redirect
from connexion import FlaskApp
from connexion.resolver import RestyResolver
from connexion.options import SwaggerUIOptions

_swagger_ui_options = SwaggerUIOptions(
    swagger_ui=True,
    swagger_ui_path="/docs",
)

app = FlaskApp(__name__)

app.add_api(
    Path.cwd() / "swagger.yaml",
    base_path="/api/v0",
    swagger_ui_options=_swagger_ui_options,
    resolver=RestyResolver('src.api.v0.controllers')
)

@app.route('/')
def index():
    return redirect('/api/v0/docs')
