from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('session/create/', views.create_session, name='create_session'),
    path('session/<str:session_id>/add_message/', views.add_message, name='add_message'),
    path('session/<str:session_id>/update_message/<str:message_id>/', views.update_message, name='update_message'),
    path('cache/check_and_cache/', views.check_and_cache, name='check_and_cache'),
]