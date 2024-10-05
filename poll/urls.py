from . import views
from django.urls import path

urlpatterns = [
    path('',views.index),
    path('create_poll/',views.create_poll,name="create_poll"),
    path('edit_poll/<int:poll_id>',views.edit_poll,name="edit_poll"),
    path('delete_poll/<int:poll_id>',views.delete_poll,name="delete_poll"),
    path('vote/<int:poll_id>',views.vote,name="vote"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]

