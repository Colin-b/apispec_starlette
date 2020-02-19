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
        pass  # pragma: no cover

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
        pass  # pragma: no cover

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
        pass  # pragma: no cover

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
        pass  # pragma: no cover

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


def test_path_operations():
    app = Starlette()
    plugin = StarlettePlugin(app)
    spec = APISpec(
        title="Test API", version="0.0.1", openapi_version="2.0", plugins=[plugin]
    )
    spec.path(
        "/test", operations={"get": {"responses": {"200": {"description": "ok"}}}}
    )
    spec.path(
        "/test_overriden",
        operations={"get": {"responses": {"200": {"description": "ok2"}}}},
    )

    @app.route("/test")
    def test_endpoint(request):
        pass  # pragma: no cover

    @app.route("/test_without_response")
    def test_endpoint_without_response(request):
        pass  # pragma: no cover

    @app.route("/test_overriden")
    def test_endpoint_with_overriden_response(request):
        """
        responses:
            200:
                description: "non ok"
        """
        pass  # pragma: no cover

    for endpoint in plugin.endpoints():
        spec.path(endpoint.path, endpoint=endpoint)

    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {
            "/test": {
                "get": {
                    "operationId": "get_test_endpoint",
                    "responses": {"200": {"description": "ok"}},
                }
            },
            "/test_overriden": {
                "get": {
                    "operationId": "get_test_endpoint_with_overriden_response",
                    "responses": {"200": {"description": "ok2"}},
                }
            },
            "/test_without_response": {
                "get": {"operationId": "get_test_endpoint_without_response"}
            },
        },
        "swagger": "2.0",
    }


def test_path_summary():
    app = Starlette()
    plugin = StarlettePlugin(app)
    spec = APISpec(
        title="Test API", version="0.0.1", openapi_version="2.0", plugins=[plugin]
    )

    @app.route("/test")
    def test_endpoint(request):
        """This is the expected summary"""
        pass  # pragma: no cover

    @app.route("/test_with_doc")
    def test_endpoint_with_doc(request):
        """
        This is the expected summary 2
        ---
        responses:
            200:
                description: "ok"
        """
        pass  # pragma: no cover

    for endpoint in plugin.endpoints():
        spec.path(endpoint.path, endpoint=endpoint)

    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {
            "/test": {
                "get": {
                    "operationId": "get_test_endpoint",
                    "summary": "This is the expected summary",
                }
            },
            "/test_with_doc": {
                "get": {
                    "summary": "This is the expected summary 2",
                    "operationId": "get_test_endpoint_with_doc",
                    "responses": {"200": {"description": "ok"}},
                }
            },
        },
        "swagger": "2.0",
    }
