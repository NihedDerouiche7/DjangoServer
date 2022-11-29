from django.urls import include, path
from . import views
from .views import InputView


urlpatterns = [
    path('', views.index, name='index'),
    path("input/", InputView.as_view()),
]