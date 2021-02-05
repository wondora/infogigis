from django.http.response import JsonResponse
from memo.forms import MemoForm
from memo.models import Memo
from django.template.loader import render_to_string
from django.http import HttpResponse

def memo(request):
    data = dict()
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid:
            form.save()
            data['form_is_valid'] = True
            memos = Memo.objects.all()[:1].values('id','created_date','title','content')
            memos = list(memos)
            data['memos'] = memos
    # else:
    #     data['form_is_valid'] = False
    #     form = MemoForm()
    #     context = {'form':form}
    #     template_name = 'memo/memo.html'
    #     
        
    return JsonResponse(data, safe=False)

def del_memo(request, pk):
    data = dict()
    del_memo = Memo.objects.get(pk=pk)
    del_memo.delete()
    data['pk'] = pk
    return JsonResponse(data)