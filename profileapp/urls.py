from django.urls import path
from profileapp.views import ProfileCV, ProfileUV

app_name = 'profileapp'

urlpatterns = [
	path('create/', ProfileCV.as_view(), name='create'),
	path('create/<int:pk>', ProfileUV.as_view(), name='update'),
]