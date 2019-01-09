from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import api_root, UserProfile, UserInfo, UserCreate
from .views import NoteViewSet, NotebookViewSet, TagViewSet

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
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^jwt-auth/', obtain_jwt_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^', include(router.urls)),
]
