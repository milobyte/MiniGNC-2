from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='gui-home'),
    path('figure.html', views.graph, name='gui-graph')
]
