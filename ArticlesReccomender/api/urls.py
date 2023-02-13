from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include, re_path

router = DefaultRouter()

router.register(r'article', ArticleViewSet, basename='article')


urlpatterns = router.urls

urlpatterns += [
]