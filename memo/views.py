from django.http.response import JsonResponse
from memo.forms import MemoForm
from memo.models import Memo
from django.views.generic import ListView

def memo(request):
    data = dict()
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid:
            form.save()
            data['form_is_valid'] = True
            memos = Memo.objects.first()
            memos = memos.__dict__
            memos['_state'] = 1 # del memos['_state']  del에서 문법에러남.
            data['memos'] = memos
    # else:
    #     data['form_is_valid'] = False
    #     form = MemoForm()
    #     context = {'form':form}
    #     template_name = 'memo/memo.html'
    #     data['html_form'] = render_to_response(template_name, context, request=request)
        
    return JsonResponse(data)
