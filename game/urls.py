from django.conf.urls import url
from django.views.generic import TemplateView
from game import views


urlpatterns = [
    url(r'^start', views.start_game, name='start'),
    url(r'^loop', views.game_loop, name='loop'),
    url(r'^play', views.initial_load, name='play'),
    url(r'^end', views.end_of_game, name='end'),
    url(r'^', TemplateView.as_view(template_name="index.html")),
]