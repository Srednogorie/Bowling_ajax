from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^play', views.game_loop, name='play'),
    url(r'^total-score', views.total_score, name='total_score'),
    url(r'^game', views.BowlingGameGameView.as_view(), name='game'),
    url(r'^model', views.BowlingGameModelView.as_view(), name='model'),
    url(r'^start', views.start_game, name='start_game')
]