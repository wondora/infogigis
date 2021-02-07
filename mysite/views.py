from django.contrib.auth.views import LoginView
from memo.models import Memo
from django.core.cache import cache
import json

class LoginView(LoginView):
	template_name='accountapp/login.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) 
		memos =  cache.get('memos')
		if not memos:
			memos = Memo.objects.all()[:20]
			cache.set('memos', memos)

		context['memos'] = memos
		return context 	
			

