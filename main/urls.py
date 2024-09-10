from django.urls import path
from . import views
from databases import postgres_users

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('postgres/', postgres_users, name='postgres'),
    path('logout/', views.logout_view, name='logout')

]
