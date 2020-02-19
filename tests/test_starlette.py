from apispec import BasePlugin
from starlette.applications import Starlette
from starlette.testclient import TestClient

from apispec_starlette import add_swagger_json_endpoint


def test_default_swagger_json_endpoint():
    app = Starlette()
    add_swagger_json_endpoint(app)

    @app.route("/test")
    def test_endpoint(request):
        """
        responses:
            200:
                description: "ok"
        """
        pass  # pragma: no cover

    @app.route("/test_without_doc")
    def test_endpoint_without_doc(request):
        pass  # pragma: no cover

    client = TestClient(app)
    response = client.get("/swagger.json")
    assert response.json() == {
        "info": {"title": "My API", "version": "0.0.1"},
        "paths": {
            "/test": {
                "get": {
                    "operationId": "get_test_endpoint",
                    "responses": {"200": {"description": "ok"}},
                }
            },
            "/test_without_doc": {
                "get": {"operationId": "get_test_endpoint_without_doc"}
            },
        },
        "swagger": "2.0",
    }


def test_swagger_json_endpoint_parameters():
    app = Starlette()

    class DummyPlugin(BasePlugin):
        pass

    plugin = DummyPlugin()

    spec = add_swagger_json_endpoint(
        app,
        title="Test API",
        version="1.0.0",
        plugins=[plugin],
        info={"x-test": "test field"},
    )

    assert plugin in spec.plugins

    @app.route("/test")
    def test_endpoint(request):
        """
        responses:
            200:
                description: "ok"
        """
        pass  # pragma: no cover

    @app.route("/test_without_doc")
    def test_endpoint_without_doc(request):
        pass  # pragma: no cover

    client = TestClient(app)
    response = client.get("/swagger.json")
    assert response.json() == {
        "info": {"title": "Test API", "version": "1.0.0", "x-test": "test field"},
        "paths": {
            "/test": {
                "get": {
                    "operationId": "get_test_endpoint",
                    "responses": {"200": {"description": "ok"}},
                }
            },
            "/test_without_doc": {
                "get": {"operationId": "get_test_endpoint_without_doc"}
            },
        },
        "swagger": "2.0",
    }


def test_swagger_json_endpoint_with_x_forwarded_prefix_header():
    app = Starlette()
    add_swagger_json_endpoint(app)

    client = TestClient(app)
    response = client.get("/swagger.json", headers={"X-Forwarded-Prefix": "/test"})
    assert response.json() == {
        "info": {"title": "My API", "version": "0.0.1"},
        "basePath": "/test",
        "paths": {},
        "swagger": "2.0",
    }
