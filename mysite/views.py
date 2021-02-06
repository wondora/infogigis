from django.contrib.auth.views import LoginView
from memo.models import Memo

class LoginView(LoginView):
	template_name='accountapp/login.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 
		context['memos'] = Memo.objects.all()[:10]
		return context 


