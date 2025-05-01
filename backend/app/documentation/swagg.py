from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_swagger_ui import get_swaggerui_blueprint
from backend.app.others.constants import Documentation

from backend.app.models.response_models import ProfileResponseSchema


swagger_ui_blueprint = get_swaggerui_blueprint(
    Documentation.SWAGGER_URL, Documentation.API_URL, config={"app_name": "Morons App"}
)


def create_tags(spec):
    """Создаем теги.

    :param spec: объект APISpec для сохранения тегов
    """
    tags = Documentation.TAGS

    for tag in tags:
        print(f"Добавляем тег: {tag['name']}")
        spec.tag(tag)


def load_docstrings(spec, app):
    """Загружаем описание API.

    :param spec: объект APISpec, куда загружаем описание функций
    :param app: экземпляр Flask приложения, откуда берем описание функций
    """
    for fn_name in app.view_functions:
        if fn_name == "static":
            continue
        print(f"Загружаем описание для функции: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


def get_apispec(app):
    """Формируем объект APISpec.

    :param app: объект Flask приложения
    """
    spec = APISpec(
        title="MoronsProj",
        version="1.0.0",
        openapi_version="3.0.3",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    spec.components.schema("Out", schema=ProfileResponseSchema)
    # spec.components.schema("Output", schema=OutputSchema)
    # spec.components.schema("Error", schema=ErrorSchema)

    create_tags(spec)

    load_docstrings(spec, app)

    return spec
