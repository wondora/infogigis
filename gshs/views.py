from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from gshs.models import *
from django.views.generic import ListView, CreateView, UpdateView
from django.db.models import Q
from gshs.forms import InfogigiForm, RepairForm, ProductbuyForm, GigirentalForm, PeopleForm, SoftwarerentalForm, SoftwarestockForm, BupumchangeForm, PhotoForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from gshs.resources import InfogigiResource
from django.http import HttpResponse
import xlwt
from django.db.models import Value as V
from django.db.models.functions import Concat
from datetime import datetime, timezone 
from gshs.forms import PhotoInlineFormSet, PlaceImageFormSet
from django.urls import reverse_lazy
# from django.utils import timezone
from django.db import transaction 
import pytz
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib import messages


class InfogigiLV(ListView): 
    template_name = 'gshs/infogigi/gigihome.html'    
    paginate_by = 10   
 
    def get_queryset(self, **kwargs):
        self.gigigubun = self.kwargs['gigigubun']
        if self.gigigubun == 'all':
            queryset = Infogigi.objects.filter(status=True).select_related('productgubun','people','place')
        else:
             queryset = Infogigi.objects.filter(productgubun__sub_division=self.gigigubun, status=True).select_related('productgubun', 'people', 'place')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
              
        gigi = Productgubun.objects.filter(main_division='infogigi').values('sub_division')      
        context["productgubun"] =gigi 
        context["gigigubun"] = self.gigigubun 
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 7 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['gigi_count'] = paginator.count

        return context

class SearchinfoLV(ListView):    
    template_name = 'gshs/infogigi/gigihome.html'  
    paginate_by = 10    

    def get_queryset(self, **kwargs):
        # self.gigigubun = self.kwargs['gigigubun']
        self.word = self.request.GET.get('word')
        post_list = Infogigi.objects.filter(Q(status=True), Q(people__name__contains=self.word) | Q(ip__contains=self.word) | Q(place__room__contains=self.word))
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gigi = Productgubun.objects.filter(main_division='infogigi')
        context["productgubun"] =gigi
        context["gigigubun"] = 'all'
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 7 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['gigi_count'] = paginator.count
        context['word'] = self.word
       
        return context

@login_required(login_url='/accounts/login/')
def save_infogigi_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()  
            if form.instance.productgubun.main_division == 'productbuy':
                Softwarestock.objects.create(model = form.instance.model, count = form.instance.count, remain = form.instance.count, price = form.instance.price)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False    
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='/accounts/login/')
def create_infogigi(request):
    # creatview 사용시 initial={'gubun':'Notebook} 초기값 줄 수 있다.
    if request.method == 'POST':
        form = InfogigiForm(request.POST)
    else:
        form = InfogigiForm()
    return save_infogigi_form(request, form, 'gshs/infogigi/partial-infogigi-create.html')

@login_required
def create_productbuy(request):
    if request.method == 'POST':
        form = ProductbuyForm(request.POST)
    else:
        form = ProductbuyForm()
    return save_infogigi_form(request, form, 'gshs/productbuy/partial-productbuy-create.html')

@login_required
def update_infogigi(request, pk):
    infogigi = get_object_or_404(Infogigi, pk=pk)    
    if request.method == 'POST':
        form = InfogigiForm(request.POST, instance=infogigi)
    else:
        form = InfogigiForm(instance=infogigi)
    return save_infogigi_form(request, form, 'gshs/infogigi/partial-infogigi-update.html')

@login_required
def update_productbuy(request, pk):
    productbuy = get_object_or_404(Productbuy, pk=pk)    
    if request.method == 'POST':
        form = ProductbuyForm(request.POST, instance=productbuy)
    else:
        form = ProductbuyForm(instance=productbuy)
    return save_infogigi_form(request, form, 'gshs/productbuy/partial-productbuy-update.html')

@login_required
def delete_infogigi(request, pk):
    infogigi = get_object_or_404(Infogigi, pk=pk)
    infogigi.status = 0
    infogigi.save()   
    return redirect('gshs:infogigi_list', gigigubun='all')

@login_required
def delete_productbuy(request, pk):
    productbuy = get_object_or_404(Productbuy, pk=pk)
    productbuy.delete()
    return redirect('gshs:productbuy_list')

@login_required
def delete_people(request, pk):
    people = get_object_or_404(People, pk=pk)
    people.status = 0
    return redirect('gshs:people_list')

@login_required
def suri_infogigi(request):
    data = dict()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():            
            form.save() 
            if request.FILES:
                try:
                    for img in request.FILES.getlist('images'):
                        # Photo 객체를 하나 생성한다.
                        photo = Photo()
                        # 외래키로 현재 생성한 Repair의 기본키를 참조한다.
                        photo.suri = form.instance
                        # imgs로부터 가져온 이미지 파일 하나를 저장한다.
                        photo.image = img
                        # 데이터베이스에 저장
                        photo.save()   
                # except Exception as ex: #에러 이름을 모를때
                #     print('에러가 발생 했습니다', ex) 
                except:
                    pass #이미지가 없어도 그냥 지나가도록
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False   
    else:
        suri_number = request.GET.get('number')
        # form = RepairForm()
        template_name = 'gshs/suri/partial-suri-create.html'  
        context = {'suri_number': suri_number} 
        data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def suri_place(request):
    data = dict()
    if request.method == 'POST':
        form = RepairForm(request.POST)
        if form.is_valid():            
            form.save() 
            if request.FILES:
                try:
                    for img in request.FILES.getlist('images'):
                        # Photo 객체를 하나 생성한다.
                        photo = Photo()
                        # 외래키로 현재 생성한 Repair의 기본키를 참조한다.
                        photo.suri = form.instance
                        # imgs로부터 가져온 이미지 파일 하나를 저장한다.
                        photo.image = img
                        # 데이터베이스에 저장
                        photo.save()   
                # except Exception as ex: #에러 이름을 모를때
                #     print('에러가 발생 했습니다', ex) 
                except:
                    pass #이미지가 없어도 그냥 지나가도록
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False   
    else:
        place_number = request.GET.get('number')
        # form = RepairForm()
        template_name = 'gshs/suri/partial-suri-place-create.html'  
        context = {'place_number': place_number} 
        data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def bupum_infogigi(request):
    data = dict()
    if request.method == 'POST':
        form = BupumchangeForm(request.POST)
        if form.is_valid(): 
            form.save(commit=False)
            infogigi_no = request.POST.get('bupum_number')
            info = Infogigi.objects.get(pk=infogigi_no)
            form.instance.infogigi = info
            form.save()            
            data['form_is_valid'] = True     
    else:
        data['form_is_valid'] = False
        bupum_number = request.GET.get('number')
        template_name = 'gshs/bupum/partial-bupum-create.html'  
        form = BupumchangeForm()
        # bupum_name = Productbuy.objects.filter(productgubun__sub_division='CONSUMABLE')
        context = {'bupum_number': bupum_number, 'form': form} 
        data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def update_bupum(request, pk):
    data = dict()
    bupum = get_object_or_404(Bupumchange, pk=pk)    
    if request.method == 'POST':
        form = BupumchangeForm(request.POST, instance=bupum)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True 
    else:
        data['form_is_valid'] = False
        template_name = 'gshs/bupum/partial-bupum-update.html'  
        form = BupumchangeForm(instance=bupum)
        context = {'form': form} 
        data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def delete_bupum(request, pk):
    bupum = get_object_or_404(Bupumchange, pk=pk)    
    bupum.delete()   
    return redirect('gshs:bupum_list')

@login_required
def suri_delete(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    repair.delete()       
    return redirect('gshs:suri_list')

@login_required
def export_excel(request):
    gigigubun = request.GET.get('gigigubun')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + gigigubun +'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(gigigubun)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['productgubun','buy_date','people','place','maker','model','ip','bigo']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Infogigi.objects.filter(productgubun__sub_division=gigigubun).values_list('productgubun','buy_date','people__name',Concat(V('['),'place__building',V(']'),'place__room'),'maker','model','ip','bigo')

    for row in rows:
        row_num+= 1        
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response

@login_required
def jaego_infogigi(request, pk):
    Infogigi.objects.filter(id=pk).update(status=0)
    Jaego.objects.create(infogigi_id=pk)
    return JsonResponse({'data':True})

@login_required
def jaego_rental(request):
    data = dict()  
    if request.method == 'POST':
        form = GigirentalForm(request.POST)
        pk = request.POST.get('transfer_no')
        if form.is_valid():
            Jaego.objects.filter(id=pk).update(rental_status="no")
            form.instance.jaego = Jaego.objects.get(id=pk)
            form.people = form.cleaned_data['people']
            form.place = form.cleaned_data['place']
            form.bigo = form.cleaned_data['bigo']
            form.save()            
            data['form_is_valid'] = True                  
            
    else: 
        data['form_is_valid'] = False       
        jaego_no = request.GET.get('number')        
        form = GigirentalForm()
        template_name = 'gshs/jaego/partial-jaego-rental.html'   
        context = {'form':form, 'transfer_no': jaego_no}              
        data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def gigirental_receive(request, pk): 
    tz = pytz.timezone('Asia/Seoul')
    Num = Gigirental.objects.filter(id=pk).values('jaego') 
    Jaego.objects.filter(id=Num[0]['jaego']).update(rental_status='yes') 
    Gigirental.objects.filter(id=pk).update(due_date=datetime.now(tz).strftime("%Y-%m-%d"))   
    return JsonResponse({'data':True})

@login_required
def gigirental_delete(rquest, pk):
    result = get_object_or_404(Gigirental, pk=pk) 
    result.delete()  
    return JsonResponse({'data':True})

class RepairLV(ListView):    
    queryset = Repair.objects.all().select_related('infogigi')  
    template_name = 'gshs/suri/gigisuri.html'    
    paginate_by = 6       

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        

        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        context['modal_gubun'] = 'modal-suri'
        return context   

def repairpk_list(request, pk):    
    suri_list = Repair.objects.filter(id=pk).select_related('infogigi') 
    print(suri_list)
    return render(request, 'gshs/suri/gigisuri.html', {'object_list':suri_list})

class SearchRepairLV(ListView):    
    template_name = 'gshs/suri/gigisuri.html'  
    paginate_by = 10   

    def get_queryset(self):
        word = self.request.GET.get('word')
        post_list = Repair.objects.select_related('infogigi').filter(Q(infogigi__model__icontains=word)|Q(created_date__icontains=word))
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        word = self.request.GET.get('word')     
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['word'] = word        
        return context

class RepairPhotoUV(LoginRequiredMixin, UpdateView):    
    queryset = Repair.objects.all().select_related('infogigi')
    fields = ('infogigi', 'cause', 'result', 'price', 'bigo')
    success_url = reverse_lazy('gshs:suri_list')
    template_name = 'gshs/suri/partial-suri-update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PhotoInlineFormSet(instance=self.object)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            items = Photo.objects.filter(suri=form.instance.pk)
            for item in items:
                if not item.image:
                    item.delete()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductbuyLV(ListView):
    model = Productbuy
    template_name = 'gshs/productbuy/productbuy.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['modal_gubun'] = 'modal-productbuy'

        return context

class SearchProductBuyLV(ListView):    
    template_name = 'gshs/productbuy/productbuy.html'  
    paginate_by = 10   

    def get_queryset(self):
        word = self.request.GET.get('word')
        post_list = Productbuy.objects.filter(model__icontains=word)
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        word = self.request.GET.get('word')     
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['word'] = word        
        return context

class JaegoLV(ListView):
    queryset = Jaego.objects.filter(not_use=False).select_related('infogigi')
    template_name = 'gshs/jaego/jaego.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['modal_gubun'] = 'modal-rental'

        return context

class SearchJaegoLV(ListView):    
    template_name = 'gshs/jaego/jaego.html'  
    paginate_by = 10   

    def get_queryset(self):
        word = self.request.GET.get('word')
        post_list = Jaego.objects.select_related('infogigi').filter(Q(infogigi__model__icontains=word)|Q(created_date__icontains=word))
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        word = self.request.GET.get('word')     
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['word'] = word        
        return context

@login_required
def jaego_notuse(request, pk):
    Jaego.objects.filter(id=pk).update(not_use=True)
    return redirect('gshs:jaego_list')

class GigirentalLV(ListView):
    queryset = Gigirental.objects.all().select_related('jaego','people','place')
    template_name = 'gshs/gigirental/gigirental.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
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

def productgubun_select(request):
    queryset = Productgubun.objects.all()
    query = request.GET.get('q')
    queryset = queryset.filter(sub_division__icontains=query)
    results = [
        {
            'id': productgubun.id,
            'text': productgubun.sub_division,
        } for productgubun in queryset
    ]

    data = {'results': results,}
    return JsonResponse(data, json_dumps_params = {'ensure_ascii': False})

class PeopleLV(ListView):
    queryset = People.objects.filter(status=True)
    template_name = 'gshs/people/people.html'
    form_class = PeopleForm
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
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

class SearchpeopleLV(ListView):    
    template_name = 'gshs/people/people.html' 
    paginate_by = 10   

    def get_queryset(self):
        word = self.request.GET.get('word')
        post_list = People.objects.filter(Q(status=True), Q(name__icontains=word))
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        word = self.request.GET.get('word')     
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['word'] = word        
        return context

class PeopleCV(LoginRequiredMixin, CreateView):
    template_name = 'gshs/people/people-create.html'
    success_url = reverse_lazy('gshs:people_list') 
    form_class = PeopleForm

    def form_valid(self, form):
        return super().form_valid(form)

class PeopleUV(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('accountapp:login')
    template_name = 'gshs/people/people-create.html'
    success_url = reverse_lazy('gshs:people_list') 
    form_class = PeopleForm

    def get_object(self, **kwargs):
        id_= self.kwargs.get('pk')
        return get_object_or_404(People, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

class SoftwarestockLV(ListView):
    queryset = Softwarestock.objects.all()
    template_name = 'gshs/softwarestock/softwarestock.html'
    form_class = SoftwarestockForm
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range  
        context['modal_gubun'] = 'modal-softwarerental'
        return context

@login_required
def create_softwarestock(request):    
    data = dict()
    if request.method == 'POST':
        form = SoftwarestockForm(request.POST)
        if form.is_valid(): 
            form.save(commit=False)
            form.instance.remain = form.instance.count
            form.save()   
            data['form_is_valid'] = True                    
        else:
            data['form_is_valid'] = False
    else:
        template_name = 'gshs/softwarestock/softwarestock-create.html'  
        form = SoftwarestockForm()
        context = {'form': form} 
        data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

@login_required
def software_rental(request):
    data = dict()  
    if request.method == 'POST':
        form = SoftwarerentalForm(request.POST)
        pk = request.POST.get('transfer_no')
        if form.is_valid():
            stock_count = Softwarestock.objects.filter(id=pk).values('remain')
            remain_count = stock_count[0]['remain'] - form.cleaned_data['count']
            Softwarestock.objects.filter(id=pk).update(remain=remain_count)                
                # add_error('count', '남은 수량 보다 많이 입력하였습니다.!')  #폼 안에 있는 기본함수 add_error(), 특정필드에 error를 넣는 함수               
            form.instance.softwarestock = Softwarestock.objects.get(id=pk)
            form.save()  
            data['form_is_valid'] = True 
        else:      
            data['form_is_valid'] = False 
    else:
        software_no = request.GET.get('number')        
        form = SoftwarerentalForm()
        template_name = 'gshs/softwarestock/softwarestock-rental.html'   
        context = {'form':form, 'transfer_no': software_no}              
        data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)

class SoftwarerentalLV(ListView):
    queryset = Softwarerental.objects.select_related('softwarestock', 'people', 'place').all()
    template_name = 'gshs/softwarerental/softwarerental.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
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

@login_required
def softwarerental_receive(request, pk):
    tz = pytz.timezone('Asia/Seoul')
    Num = Softwarerental.objects.get(id=pk) 
    remaining = Num.count + Num.softwarestock.remain
    Softwarestock.objects.filter(id=Num.softwarestock_id).update(remain=remaining)
    Softwarerental.objects.filter(id=pk).update(due_date=datetime.now(tz).strftime("%Y-%m-%d"))   
    return JsonResponse({'data':True})

class BupumLV(ListView):
    queryset = Bupumchange.objects.all().select_related('infogigi')
    template_name = 'gshs/bupum/bupum.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        page_numbers_range = 7  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['modal_gubun'] = 'modal-bupum'

        return context

class SearchbupumLV(ListView):
    template_name = 'gshs/bupum/bupum.html'  
    paginate_by = 10    

    def get_queryset(self, **kwargs):
        # self.gigigubun = self.kwargs['gigigubun']
        self.word = self.request.GET.get('word')
        post_list = Bupumchange.objects.filter(Q(people__name__contains=self.word) | Q(ip__contains=self.word) | Q(place__room__contains=self.word)) #<------ 수정
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gigi = Productgubun.objects.all()[:4]
        context["productgubun"] =gigi
        context["gigigubun"] = 'all'
        paginator = context['paginator']
        page_numbers_range = 7  # Display only 7 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['word'] = self.word
    
        return context

class PlaceLV(ListView): 
    template_name = 'gshs/place/list-place.html'  

    def get_queryset(self, **kwargs):
        self.place_gubun = self.kwargs['place_gubun']
        self.place_number = Place.objects.get(room=self.place_gubun)
        queryset = Place.objects.filter(buseo=self.place_number.buseo).order_by('building')  
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gubun'] = self.place_number.bus
        self.place_list = self.place_number.infogigi_set.all().select_related('productgubun', 'people', 'place')
        context['place_gigi_list'] = self.place_number.infogigi_set.filter(Q(productgubun__sub_division__iexact='PRINTER') | Q(productgubun__sub_division__iexact='PROJECTOR') | Q(productgubun__sub_division__iexact='TV')).select_related('productgubun', 'people', 'place')
        context['place_people_list'] = self.place_number.infogigi_set.filter(Q(productgubun__sub_division__iexact='NOTEBOOK') | Q(productgubun__sub_division__iexact='DESKTOP')).select_related('productgubun', 'people', 'place')
        context['place_id'] = self.place_number.id
        context['place_gubun'] = self.place_number.building + ' ( ' + self.place_number.room + ' )'
        context['place_buseo_gubun'] = self.place_number.buseo
        context['place_number'] = self.place_number

        suri_data = []
        if self.place_list:
            for i in range(len(self.place_list)):
                if not self.place_list[i].repair_set.all().select_related('infogigi'):
                    continue
                suri_data.append(self.place_list[i].repair_set.all().select_related('infogigi'))
        else:
            suri_data.append(self.place_list[i].repair_set.all().select_related('place'))

        context['place_suri_list'] = suri_data

        bupum_data = [] 
        for i in range(len(self.place_list)):   
            if not self.place_list[i].bupumchange_set.all().select_related('infogigi'):
                continue
            bupum_data.append(self.place_list[i].bupumchange_set.all().select_related('infogigi'))
        context['place_bupum_list'] = bupum_data

        return context

@login_required
def photo_place(request, pk):    
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":        
        form = PhotoForm(request.POST, request.FILES)    
        if form.is_valid():
            for img in request.FILES.getlist('images'):                        
                photo = Photo(image=img, place=form.instance.place)
                photo.save() 

        place_gubun = Place.objects.get(id=pk)               
        return redirect('gshs:list_place',  place_gubun=place_gubun.room)
        
    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = PhotoForm()
        context = {'form':form, 'place_id': pk}
        return render(request, 'gshs/place/edit_place_image.html', context)        


class PlacePhotoUV(LoginRequiredMixin, UpdateView):    
    model = Place
    fields = ('building', 'room', 'buseo') 
    template_name = 'gshs/place/photo-update-place.html'

    def get_success_url(self):
        place_id = self.get_object()
        return reverse_lazy('gshs:list_place', kwargs={'place_gubun':place_id.room})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PlaceImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PlaceImageFormSet(instance=self.object)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                formset.instance = self.object
                formset.save()

                items = Photo.objects.filter(place=form.instance.pk)
                for item in items:
                    if not item.image:
                        item.delete()
            return redirect(self.get_success_url())        
        else:
            return self.render_to_response(self.get_context_data(form=form))