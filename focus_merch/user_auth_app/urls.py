from django.urls import path
from . import views

app_name = 'user_auth_app'

urlpatterns  = [
    path('sign-up', views.register_view, name='sign-up'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_page, name='logout'),
]