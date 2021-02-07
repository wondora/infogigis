from django.http.response import JsonResponse
from memo.forms import MemoForm
from memo.models import Memo
from django.template.loader import render_to_string

def memo(request):
    data = dict()
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid:
            form.save()
            data['form_is_valid'] = True
            memos = Memo.objects.all()[:1].values('id','created_date','title')
            memos = list(memos)
            data['memos'] = memos
   
    return JsonResponse(data, safe=False)

def del_memo(request, pk):
    data = dict()
    del_memo = Memo.objects.get(pk=pk)
    del_memo.delete()
    data['pk'] = pk
    return JsonResponse(data)

def search_memo(request):
    data = dict()
    search = request.POST['search']
    result = Memo.objects.filter(title__contains=search)
    data['search'] = list(result.values())
    return JsonResponse(data, safe=False)

