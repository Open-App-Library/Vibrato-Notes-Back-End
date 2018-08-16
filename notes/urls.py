from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import NoteList, NoteDetail

urlpatterns = [
	url(r'^$', NoteList.as_view()),
	url(r'^(?P<pk>[0-9]+)/$', NoteDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
