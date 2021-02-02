from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from profileapp.models import Profile
from profileapp.forms import ProfileCreationForm
from django.utils.decorators import method_decorator
from profileapp.decorators import profile_ownership_required
 

class ProfileCV(CreateView):
	model = Profile	
	context_object_name = 'target_profile'
	form_class = ProfileCreationForm
	success_url = reverse_lazy('home')
	template_name = 'profileapp/create.html'

	def form_valid(self, form):
		temp_profile = form.save(commit=False)
		temp_profile.user = self.request.user
		temp_profile.save()
		return super().form_valid(form)

@method_decorator(profile_ownership_required, 'get')	
@method_decorator(profile_ownership_required, 'post')	
class ProfileUV(UpdateView):
	model = Profile	
	context_object_name = 'target_profile'
	form_class = ProfileCreationForm
	success_url = reverse_lazy('home')
	template_name = 'profileapp/update.html'