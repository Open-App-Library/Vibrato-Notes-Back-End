from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import NoteList, NoteDetail, UserList, UserDetail

urlpatterns = [
	url(r'^$', NoteList.as_view()),
	url(r'^(?P<pk>[0-9]+)/$', NoteDetail.as_view()),
	url(r'^users/$', UserList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
	url(r'^api-auth/', include('rest_framework.urls')),
]

