from django.urls import path
from . import views
from databases import postgres_users

urlpatterns = [
    # path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('', views.register_view, name='register'),
    path('todo/',views.todo,name='todo'),
    # path('exb/',views.exb,name='exb'),
    path('userlist/',views.userlist,name='userlist'),
    # path('delete_exhibition/', views.delete_exhibition, name='delete_exhibition'),
    path('assign/', views.assign, name='assign'),
    path('postgres/', postgres_users, name='postgres'),

]
