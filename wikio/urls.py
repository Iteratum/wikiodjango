from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("get_data/<int:id>", views.get_data, name="get_data"),
    path("", views.index, name="index"),
    path("randoms/", views.randoms, name="randoms"),
    path("newPage/", views.newPage, name='newPage'),
    path("editPage/", views.editPage, name='editPage'),
    path("search/", views.search, name="search"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
