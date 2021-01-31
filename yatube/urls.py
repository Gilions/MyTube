from django.contrib.flatpages import views
from django.urls import include, path
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken import views as aviews


handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include("users.urls")),
    path('auth/', include("django.contrib.auth.urls")),
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='about-author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='about-spec'),
    path('api-token-auth/', aviews.obtain_auth_token),
    path("", include("posts.urls")),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
