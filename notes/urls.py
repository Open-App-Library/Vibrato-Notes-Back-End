from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from .views import api_root, UserProfile, UserInfo, UserCreate
from .views import NoteViewSet, NotebookViewSet, TagViewSet
from .views import oauth_code

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'notebooks', NotebookViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    url(r'^$', api_root),
    url(r'^profile/$', UserProfile.as_view(), name="user-profile"),
    url(r'^new-user/$', UserCreate.as_view(), name="user-create"),
    url(r'^username/(?P<username>[\w\-\_\n]+)/$',
        UserInfo.as_view(),
        name="user-info"),
    url(r'^session-auth/', include('rest_framework.urls')),

    # OAuth2
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^oauth-code/', oauth_code),


]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^', include(router.urls)),
    # API Authentication
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
