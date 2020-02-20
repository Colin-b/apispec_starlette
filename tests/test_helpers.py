from apispec import APISpec
from starlette.applications import Starlette

from apispec_starlette import (
    StarlettePlugin,
    document_response,
    document_oauth2_authentication,
    document_endpoint_oauth2_authentication,
)


def test_response_documentation():
    app = Starlette()
    plugin = StarlettePlugin(app)
    spec = APISpec(
        title="Test API", version="0.0.1", openapi_version="2.0", plugins=[plugin]
    )
    document_response(
        spec,
        endpoint="/test",
        method="get",
        status_code=200,
        response={"description": "ok"},
    )

    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {"/test": {"get": {"responses": {"200": {"description": "ok"}}}}},
        "swagger": "2.0",
    }


def test_oauth2_authentication_documentation():
    app = Starlette()
    plugin = StarlettePlugin(app)
    spec = APISpec(
        title="Test API", version="0.0.1", openapi_version="2.0", plugins=[plugin]
    )
    document_oauth2_authentication(
        spec,
        authorization_url="http://test",
        flow="implicit",
        scopes={"scope1": "Description of scope1", "scope2": "Description of scope2"},
    )

    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {},
        "securityDefinitions": {
            "oauth2": {
                "authorizationUrl": "http://test",
                "flow": "implicit",
                "scopes": {
                    "scope1": "Description of " "scope1",
                    "scope2": "Description of " "scope2",
                },
                "type": "oauth2",
            }
        },
        "swagger": "2.0",
    }


def test_endpoint_oauth2_authentication_documentation():
    app = Starlette()
    plugin = StarlettePlugin(app)
    spec = APISpec(
        title="Test API", version="0.0.1", openapi_version="2.0", plugins=[plugin]
    )
    document_endpoint_oauth2_authentication(
        spec, endpoint="/test", method="get", required_scopes=["scope1", "scope2"]
    )

    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {
            "/test": {
                "get": {
                    "responses": {
                        "401": {
                            "description": "No "
                            "permission "
                            "-- "
                            "see "
                            "authorization "
                            "schemes",
                            "schema": {"type": "string"},
                        },
                        "403": {
                            "description": "Request "
                            "forbidden "
                            "-- "
                            "authorization "
                            "will "
                            "not "
                            "help",
                            "schema": {"type": "string"},
                        },
                    },
                    "security": [{"oauth2": ["scope1", "scope2"]}],
                }
            }
        },
        "swagger": "2.0",
    }


def test_endpoint_oauth2_authentication_full_documentation():
    app = Starlette()
    plugin = StarlettePlugin(app)
    spec = APISpec(
        title="Test API", version="0.0.1", openapi_version="2.0", plugins=[plugin]
    )
    document_oauth2_authentication(
        spec,
        authorization_url="http://test",
        flow="implicit",
        scopes={"scope1": "Description of scope1", "scope2": "Description of scope2"},
    )
    document_endpoint_oauth2_authentication(
        spec,
        endpoint="/test",
        method="get",
        required_scopes=["scope1", "scope2"],
        unauthorized_status_code=400,
        forbidden_status_code=402,
    )

    @app.route("/test")
    def endpoint():
        """
        responses:
            200:
                description: ok
                type: string
        """
        pass  # pragma: no cover

    assert spec.to_dict() == {
        "info": {"title": "Test API", "version": "0.0.1"},
        "paths": {
            "/test": {
                "get": {
                    "responses": {
                        "400": {
                            "description": "No "
                            "permission "
                            "-- "
                            "see "
                            "authorization "
                            "schemes",
                            "schema": {"type": "string"},
                        },
                        "402": {
                            "description": "Request "
                            "forbidden "
                            "-- "
                            "authorization "
                            "will "
                            "not "
                            "help",
                            "schema": {"type": "string"},
                        },
                    },
                    "security": [{"oauth2": ["scope1", "scope2"]}],
                }
            }
        },
        "securityDefinitions": {
            "oauth2": {
                "authorizationUrl": "http://test",
                "flow": "implicit",
                "scopes": {
                    "scope1": "Description of " "scope1",
                    "scope2": "Description of " "scope2",
                },
                "type": "oauth2",
            }
        },
        "swagger": "2.0",
    }
