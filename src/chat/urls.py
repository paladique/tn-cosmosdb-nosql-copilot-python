from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('session/create/', views.create_session, name='create_session'),
    path('session/<uuid:session_id>/add_message/', views.add_message, name='add_message'),
    path('session/<uuid:session_id>/update_message/<uuid:message_id>/', views.update_message, name='update_message'),
    path('cache/check/', views.check_and_cache, name='check_and_cache'),
]