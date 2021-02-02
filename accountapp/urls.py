from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accountapp import views

app_name = 'accountapp'
urlpatterns = [
    path('create/', views.AccountCV.as_view(), name='create'),
    path('update/<int:pk>', views.AccountUV.as_view(), name='update'),
    path('delete/<int:pk>', views.AccountDV.as_view(), name='delete'),
    path('login/', LoginView.as_view(template_name='accountapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),    
]