import os

from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    Response,
)
from tartiflette import Engine

from .errors import format_errors
from .utils import load_string_template

CURDIR = os.path.dirname(__file__)


class GraphQLHandler:
    ROOT_URLS = {"", "/"}
    graphiql_template = load_string_template(
        os.path.join(CURDIR, "graphiql.html")
    )

    def __init__(self, engine: Engine, graphiql: bool, path: str):
        self.engine = engine
        self.graphiql = graphiql
        self.path = path

    async def handle_graphiql(self, request: Request) -> Response:
        text = self.graphiql_template.substitute(path=request.url.path)
        return HTMLResponse(text)

    def matches(self, path: str) -> bool:
        if not self.path:
            return path in self.ROOT_URLS
        return path == self.path

    async def __call__(self, scope, receive) -> Response:
        if not self.matches(scope["path"]):
            return PlainTextResponse("Not Found", 404)

        request = Request(scope, receive)
        background = BackgroundTasks()

        if request.method in ("GET", "HEAD"):
            if "text/html" in request.headers.get("Accept", ""):
                if not self.graphiql:
                    return PlainTextResponse("Not Found", 404)
                return await self.handle_graphiql(request)

            data = request.query_params

        elif request.method == "POST":
            content_type = request.headers.get("Content-Type", "")

            if "application/json" in content_type:
                data = await request.json()

            elif "application/graphql" in content_type:
                body = await request.body()
                data = {"query": body.decode()}

            elif "query" in request.query_params:
                data = request.query_params

            else:
                return PlainTextResponse("Unsupported Media Type", 415)

        else:
            return PlainTextResponse("Method Not Allowed", 405)

        assert data is not None

        try:
            query = data["query"]
        except KeyError:
            return PlainTextResponse(
                "No GraphQL query found in the request", 400
            )

        context = {"req": request, "background": background}
        variables = data.get("variables")
        operation_name = data.get("operationName")

        result: dict = await self.engine.execute(
            query,
            variables=variables,
            context=context,
            operation_name=operation_name,
        )

        content = {"data": result["data"]}
        has_errors = "errors" in result
        if has_errors:
            content["errors"] = format_errors(result["errors"])
        status = 400 if has_errors else 200

        return JSONResponse(
            content=content,
            status_code=status,
            background=context["background"],
        )
