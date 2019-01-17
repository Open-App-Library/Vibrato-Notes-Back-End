from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from .views import api_root
from .views import NoteViewSet, NotebookViewSet, TagViewSet
from .views import oauth_code

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'notebooks', NotebookViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    url(r'^$', api_root),
    url(r'^session-auth/', include('rest_framework.urls')),

    # OAuth2
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^oauth-code/', oauth_code),

    url(r'^docs/', include_docs_urls(title='Vibrato Cloud API',
                                     public=True,
                                     permission_classes=(
                                         permissions.IsAuthenticatedOrReadOnly,)))
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^', include(router.urls)),
    # API Authentication
    url(r'^users/', include('djoser.urls')),
    url(r'^users/', include('djoser.urls.authtoken')),
]
