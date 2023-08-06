import functools

from graphql import graphql
from graphql.error import format_error as format_graphql_error
from starlette import status
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from starlette.types import ASGIInstance, Receive, Scope, Send

from .base import BaseApp
from .utils import get_playground_template


class GraphQLApp(BaseApp):
    def __init__(self, schema, playground: bool = True) -> None:
        self.schema = schema
        self.playground = playground

    def __call__(self, scope: Scope) -> ASGIInstance:
        return functools.partial(self.asgi, scope=scope)

    async def asgi(self, receive: Receive, send: Send, scope: Scope) -> None:
        request = Request(scope, receive=receive)
        response = await self.handle_graphql(request)
        await response(receive, send)

    async def handle_graphql(self, request: Request) -> Response:
        if request.method in ("GET", "HEAD"):
            if "text/html" in request.headers.get("Accept", ""):
                if not self.playground:
                    return PlainTextResponse(
                        "Not Found", status_code=status.HTTP_404_NOT_FOUND
                    )
            return await self.handle_playground(request)

        elif request.method == "POST":
            content_type = request.headers.get("Content-Type", "")

            if "application/json" in content_type:
                data = await request.json()
            elif "application/graphql" in content_type:
                body = await request.body()
                text = body.decode()
                data = {"query": text}
            elif "query" in request.query_params:
                data = request.query_params
            else:
                return PlainTextResponse(
                    "Unsupported Media Type",
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                )
        else:
            return PlainTextResponse(
                "Method Not Allowed", status_code=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        try:
            query = data["query"]
            variables = data.get("variables")
            operation_name = data.get("operationName")
        except KeyError:
            return PlainTextResponse(
                "No GraphQL query found in the request",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        self._debug_log(operation_name, query, variables)

        background = BackgroundTasks()
        context = {"request": request, "background": background}

        result = await self.execute(
            query, variables=variables, context=context, operation_name=operation_name
        )
        error_data = (
            [format_graphql_error(err) for err in result.errors]
            if result.errors
            else None
        )
        response_data = {"data": result.data, "errors": error_data}
        status_code = (
            status.HTTP_400_BAD_REQUEST if result.errors else status.HTTP_200_OK
        )

        return JSONResponse(
            response_data, status_code=status_code, background=background
        )

    async def handle_playground(self, request: Request) -> Response:
        text = get_playground_template(str(request.url))

        return HTMLResponse(text)

    async def execute(self, query, variables=None, context=None, operation_name=None):
        return await graphql(
            self.schema,
            query,
            variable_values=variables,
            operation_name=operation_name,
            context_value=context,
        )
