from os.path import join

from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

from error_pages.views import not_pk_error, hand404
from . import views


app_name='global_app'


file_dir = join(settings.BASE_DIR, 'global_app/templates/global_app')

urlpatterns = [
    path('subirArchivo/', views.ImageCreateView.as_view(), name='subirArchivo'),
    path('imgnotfound/', not_pk_error, name='notpk'),
    path('', views.home, name='index'),
    path('<int:pk>', views.HomeDetail.as_view()),
    *views.dir_to_url(
        file_dir,
        'detail'
    ),
    *views.dir_to_url(
        file_dir,
        views.redir_notpk
    ),
    *views.organ_patterns,
    *views.organ_error_patterns,
]