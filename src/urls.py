"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from pathlib import Path
from typing import Any

from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpRequest, HttpResponse
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView

from src.graphql_core.context import Context
from src.graphql_core.schema import schema


class GraphQLView(AsyncGraphQLView):
    async def get_context(self, request: HttpRequest, response: HttpResponse) -> Any:
        return Context(request=request, response=response)


urlpatterns = [
    path(
        "graphql/",
        csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=settings.GRAPHIQL_ENABLED, allow_queries_via_get=True)),
    ),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
if settings.DEBUG:
    import debug_toolbar

    def pyinstrument_report(request: HttpRequest) -> HttpResponse:
        with Path("pyinstrument.html").open("r") as file:
            response = HttpResponse(file.read(), content_type="text/html")
            return response

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),  # type: ignore
        path("pyinstrument/", pyinstrument_report),
        *urlpatterns,
    ]
