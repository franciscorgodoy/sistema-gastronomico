from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    path("gastos/", include("sis_gastronomico.gastos.urls", namespace="gastos")),
    path("turnos/", include("sis_gastronomico.turnos.urls", namespace="turnos")),
    path(
        "",
        login_required(TemplateView.as_view(template_name="pages/home.html")),
        name="home",
    ),
    path(
        "empleados/", include("sis_gastronomico.empleados.urls", namespace="empleados")
    ),
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("sis_gastronomico.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path(
        "productos/", include("sis_gastronomico.productos.urls", namespace="productos")
    ),
    # Your stuff: custom urls includes go here
    path("insumos/", include("sis_gastronomico.insumos.urls", namespace="insumos")),
    path("compras/", include("sis_gastronomico.compras.urls", namespace="compras")),
    path("stocks/", include("sis_gastronomico.stocks.urls", namespace="stocks")),
    path("pedidos/", include("sis_gastronomico.pedidos.urls", namespace="pedidos")),
    path(
        "proveedores/",
        include("sis_gastronomico.proveedores.urls", namespace="proveedores"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
