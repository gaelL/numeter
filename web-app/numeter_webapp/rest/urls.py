"""
REST urls module.
"""

from django.conf.urls import patterns, include, url
from rest_framework import routers
from rest.viewsets import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'superusers', SuperuserViewSet, base_name='superuser')
router.register(r'groups', GroupViewSet)
router.register(r'storages', StorageViewSet)
router.register(r'hosts', HostViewSet)
router.register(r'plugins', PluginViewSet)
router.register(r'sources', SourceViewSet)
router.register(r'views', ViewViewSet)
router.register(r'multiviews', MultiviewViewSet)
router.register(r'skeletons', SkeletonViewSet)

urlpatterns = patterns('',
    url(r'^rest/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
)
