from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginView(LoginView):
	template_name='accountapp/login.html'

	def get(self, request, *args, **kwargs):
			if self.request.user.is_authenticated:
					return HttpResponseRedirect(reverse('gshs:infogigi_list', args=('all',)))
