from apispec import APISpec
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request

from apispec_starlette import StarlettePlugin


def test_without_exception_handlers_in_app():
    app = Starlette()
    spec = APISpec(
        title="Test API",
        version="0.0.1",
        openapi_version="2.0",
        plugins=[StarlettePlugin(app)],
    )
    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {},
        "swagger": "2.0",
    }


def test_with_exception_handlers_in_app_without_status_code_but_yaml_docstring():
    async def handle_exception(request: Request, exc: HTTPException):
        """
        required:
            - message
        properties:
            message:
                type: string
                description: Description of the error.
                example: This is a description of the error.
        type: object
        """
        pass

    app = Starlette(exception_handlers={HTTPException: handle_exception})
    spec = APISpec(
        title="Test API",
        version="0.0.1",
        openapi_version="2.0",
        plugins=[StarlettePlugin(app)],
    )
    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {},
        "swagger": "2.0",
    }


def test_with_exception_handlers_in_app_with_status_code_in_yaml_docstring():
    async def handle_exception(request: Request, exc: HTTPException):
        """
        400:
            required:
                - message
            properties:
                message:
                    type: string
                    description: Description of the error.
                    example: This is a description of the error.
            type: object
        """
        pass

    app = Starlette(exception_handlers={HTTPException: handle_exception})
    spec = APISpec(
        title="Test API",
        version="0.0.1",
        openapi_version="2.0",
        plugins=[StarlettePlugin(app)],
    )
    assert spec.to_dict() == {
        "definitions": {
            "Error400": {
                "properties": {
                    "message": {
                        "description": "Description " "of " "the " "error.",
                        "example": "This is a " "description " "of the " "error.",
                        "type": "string",
                    }
                },
                "required": ["message"],
                "type": "object",
            }
        },
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {},
        "responses": {400: {"schema": {"$ref": "#/definitions/Error400"}}},
        "swagger": "2.0",
    }


def test_with_exception_handlers_in_app_with_status_code_in_handler_and_yaml_docstring():
    async def handle_exception(request: Request, exc: HTTPException):
        """
        required:
            - message
        properties:
            message:
                type: string
                description: Description of the error.
                example: This is a description of the error.
        type: object
        """
        pass

    app = Starlette(exception_handlers={400: handle_exception})
    spec = APISpec(
        title="Test API",
        version="0.0.1",
        openapi_version="2.0",
        plugins=[StarlettePlugin(app)],
    )
    assert spec.to_dict() == {
        "definitions": {
            "Error400": {
                "properties": {
                    "message": {
                        "description": "Description " "of " "the " "error.",
                        "example": "This is a " "description " "of the " "error.",
                        "type": "string",
                    }
                },
                "required": ["message"],
                "type": "object",
            }
        },
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {},
        "responses": {400: {"schema": {"$ref": "#/definitions/Error400"}}},
        "swagger": "2.0",
    }


def test_with_exception_handlers_in_app_with_status_code_in_handler_but_without_yaml_docstring():
    async def handle_exception(request: Request, exc: HTTPException):
        pass

    app = Starlette(exception_handlers={400: handle_exception})
    spec = APISpec(
        title="Test API",
        version="0.0.1",
        openapi_version="2.0",
        plugins=[StarlettePlugin(app)],
    )
    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {},
        "swagger": "2.0",
    }
