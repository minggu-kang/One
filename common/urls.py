from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


app_name = "common"

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'common/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'common/logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),

]