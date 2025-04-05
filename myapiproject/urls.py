"""
URL configuration for myapiproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from tasks.views import registration_view


def api_home(request):
    return JsonResponse({
        "message": "歡迎使用我的 Django REST API",
        "docs": "/api/docs/",
        "redoc": "/api/redoc/",
        "task api": "/api/tasks/",
        "auth": {
            "register": "/api/auth/register/",
            "login": "/api/auth/login/"
        }
    })
urlpatterns = [
    path('', api_home),
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('api/auth/register/', registration_view),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT登入
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT刷新
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
