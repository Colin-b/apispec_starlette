<h2 align="center">Plugin for APISpec handling Starlette</h2>

<p align="center">
<a href="https://pypi.org/project/apispec-starlette/"><img alt="pypi version" src="https://img.shields.io/pypi/v/apispec-starlette"></a>
<a href="https://travis-ci.com/Colin-b/apispec_starlette"><img alt="Build status" src="https://api.travis-ci.com/Colin-b/apispec_starlette.svg?branch=master"></a>
<a href="https://travis-ci.com/Colin-b/apispec_starlette"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.com/Colin-b/apispec_starlette"><img alt="Number of tests" src="https://img.shields.io/badge/tests-15 passed-blue"></a>
<a href="https://pypi.org/project/apispec-starlette/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/apispec-starlette"></a>
</p>

> This module should not be considered as stable as it is still under development.
>
> However a stable version can be expected by mid March 2020 and any issue or pull request is welcome at any time.

Provides a [plugin to use with APISpec](https://apispec.readthedocs.io/en/stable/using_plugins.html) to be able to handle [Starlette](https://www.starlette.io) endpoints.

## StarlettePlugin usage

```python
from starlette.applications import Starlette
from apispec import APISpec
from apispec_starlette import StarlettePlugin


app = Starlette()
spec = APISpec(
    title="My API",
    version="0.0.1",
    openapi_version="2.0",
    plugins=[StarlettePlugin(app)],
)
```

### Documenting responses inside endpoint docstring

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from apispec import APISpec
from apispec_starlette import StarlettePlugin


app = Starlette()
spec = APISpec(
    title="My API",
    version="0.0.1",
    openapi_version="2.0",
    plugins=[StarlettePlugin(app)],
)


@app.route("/my_endpoint")
def my_endpoint(request):
    """
    responses:
        200:
            description: "Action performed"
            schema:
                properties:
                    status:
                        type: string
                type: object
    """
    return JSONResponse({"status": "test"})
```

### Documenting responses outside of endpoint docstring

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from apispec import APISpec
from apispec_starlette import StarlettePlugin, document_response


app = Starlette()
spec = APISpec(
    title="My API",
    version="0.0.1",
    openapi_version="2.0",
    plugins=[StarlettePlugin(app)],
)


@app.route("/my_endpoint")
def my_endpoint(request):
    return JSONResponse({"status": "test"})


document_response(spec, endpoint="/my_endpoint", method="get", status_code=200, response={
    "description": "Action performed",
    "schema": {
        "properties": {"status": {"type": "string"}},
        "type": "object",
    }
})
```

### Documenting OAuth2 security outside of endpoint docstring

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires, AuthenticationBackend
from starlette.responses import JSONResponse
from apispec import APISpec
from apispec_starlette import StarlettePlugin, document_endpoint_oauth2_authentication, document_oauth2_authentication


# TODO Replace by your OAuth2 backend
app = Starlette(middleware=[Middleware(AuthenticationMiddleware, backend=AuthenticationBackend())])
spec = APISpec(
    title="My API",
    version="0.0.1",
    openapi_version="2.0",
    plugins=[StarlettePlugin(app)],
)

# TODO Adjust parameters
document_oauth2_authentication(spec, authorization_url="http://authorization_url", flow="implicit", scopes={"scope1": "Description of scope 1", "scope2": "Description of scope 2"})

@app.route("/my_endpoint")
@requires(scopes=["scope1", "scope2"])
def my_endpoint(request):
    return JSONResponse({"status": "test"})


document_endpoint_oauth2_authentication(spec, endpoint="/my_endpoint", method="get", required_scopes=["scope1", "scope2"])
```

## Add a /swagger.json endpoint

Your endpoints can be automatically discovered and documented when requesting /swagger.json

```python
from starlette.applications import Starlette
from apispec_starlette import add_swagger_json_endpoint


app = Starlette()
spec = add_swagger_json_endpoint(app=app)
```

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install apispec_starlette
```
