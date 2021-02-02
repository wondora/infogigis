from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from accountapp.forms import AccountUpdateForm
from accountapp.decorators import account_ownership_required
from django.contrib.auth.views import LoginView


has_ownership = [login_required, account_ownership_required]

class AccountCV(CreateView):
    model = User
    context_object_name = 'target_user'
    form_class = UserCreationForm
    success_url = reverse_lazy('gshs:infogigi_list', kwargs={'gigigubun': 'all'})
    template_name = 'accountapp/create.html'

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUV(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('home')
    template_name = 'accountapp/update.html'
# success_url = reverse_lazy('home') detail페이지로 갈 경우 pk가 있어야 되므로 get_success_url함수를
# 오버라이딩 해야한다.
    # def get_success_url(self):
    #     return reverse('accountapp:detail', kwargs={'pk': self.object.user.pk})
    #     self.object는 User이다.



@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDV(DeleteView):   
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'

# class LoginView(LoginView):           # 로그인
#     template_name = 'accountapp/login.html'

#     def form_invalid(self, form):
#         messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
#         return super().form_invalid(form)   