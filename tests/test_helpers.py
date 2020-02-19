from apispec import APISpec
from starlette.applications import Starlette

from apispec_starlette import StarlettePlugin, document_response


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
