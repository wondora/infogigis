from django.http.response import JsonResponse
from memo.forms import MemoForm
from memo.models import Memo
from django.core.cache import cache
from django.views.generic import ListView, UpdateView

class ListLV(ListView): 
    template_name = 'memo/memo.html'     
    paginate_by = 7   
 
    def get_queryset(self, **kwargs):
        queryset = cache.get('memos')
        if not queryset:
            queryset = Memo.objects.all()
            cache.set('memos', queryset)       
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        paginator = context['paginator']
        page_numbers_range = 5  
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
       
        return context

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

def memo(request):
    data = dict()
    form = MemoForm(request.POST)
    if form.is_valid:
        form.save()    
    return JsonResponse({'data':True})


