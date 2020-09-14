from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from apps.api.views import CategoryViewSet, CategoryNotes, SingleCategoryNote, NoteViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('notes', NoteViewSet, basename='notes')
custom_urlpatterns = [
   url(r'categories/(?P<category_pk>\d+)/notes$', CategoryNotes.as_view(), name='category_notes'),
   url(r'categories/(?P<category_pk>\d+)/notes/(?P<pk>\d+)$', SingleCategoryNote.as_view(), name='single_category_note'),
]
urlpatterns = router.urls
urlpatterns += custom_urlpatterns

