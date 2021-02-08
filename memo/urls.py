from django.urls import path
from memo import views

app_name = 'memo'
urlpatterns = [
    path('list/', views.ListLV.as_view(), name='list_memo'),
    path('', views.memo, name='memo'),
    path('delete/<int:pk>/', views.del_memo, name='del_memo'),
    path('search/', views.search_memo, name='search_memo'),
]