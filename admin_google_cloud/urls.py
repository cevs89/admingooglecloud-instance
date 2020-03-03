"""admin_google_cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from service.views import RegisterServiceViewSet, ObtainExpiringAuthToken, \
                            RegisterPhotoView, PhotoView
from start_and_stop.views import OperationServiceViews, \
                                    ListServiceViews


router = DefaultRouter()
router.register(r'service', RegisterServiceViewSet, basename='service')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    # General
    path('api/v1/obtain-token/', ObtainExpiringAuthToken.as_view()),
    path('api/v1/<str:action>/service/', OperationServiceViews.as_view()),
    path('api/v1/list/instance/', ListServiceViews.as_view()),
    path('api/v1/register/photo/', RegisterPhotoView.as_view()),

    path('api/v1/views/photo/', PhotoView.as_view()),


]
