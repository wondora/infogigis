from django import forms
from django.forms import inlineformset_factory
from gshs.models import Infogigi, Productbuy, Repair, Jaego, Photo, Gigirental, People, Softwarerental, Softwarestock, Bupumchange, Productgubun
from gshs.widgets import AutoCompleteWidget, DatePickerWidget
from django.urls import reverse_lazy

PhotoInlineFormSet = inlineformset_factory(Repair, Photo,\
    fields=['image',], extra=3)

class InfogigiForm(forms.ModelForm):  
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['productgubun'].queryset = Productgubun.objects.filter(table_name='infogigi')       


    class Meta:
        model = Infogigi
        fields = '__all__'  
        # widgets = {
        #     'productgubun': AutoCompleteWidget(ajax_url=reverse_lazy('gshs:productgubun_select')),
        #     'buy_date' : DatePickerWidget,
        # }         

class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['image'].required = False #file 값이 없더라도 view에서 유효성 검사에서 오류를 발생시키지 않도록 해준다
    #     self.fields['image'].widget.attrs.update({'class':'form-control-file'})
    #     self.fields['image'].multiple = True

class ProductbuyForm(forms.ModelForm):  
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['productgubun'].queryset = Productgubun.objects.filter(table_name='productbuy')    

    class Meta:
        model = Productbuy
        fields = '__all__'

class JaegoForm(forms.ModelForm):    
    class Meta:
        model = Jaego
        fields = '__all__'

class BupumchangeForm(forms.ModelForm):    
    class Meta:
        model = Bupumchange
        fields = ['productbuy','count','price','bigo']

class GigirentalForm(forms.ModelForm):    
    class Meta:
        model = Gigirental
        fields = ['jaego','people', 'place', 'bigo']
        widgets = {
            'jaego': forms.HiddenInput
        }

class PeopleForm(forms.ModelForm):    
    class Meta:
        model = People
        fields = '__all__'
    # def save(self, **kwargs):
    #     gigirental = super().save(commit=False)         # 부모메서드 호출 
    #     gigirental.infogigi.id = kwargs.get('infogigi_no', None)
    #     post.save()
class SoftwarestockForm(forms.ModelForm):
    class Meta:
        model = Softwarestock 
        fields = '__all__'
        
class SoftwarerentalForm(forms.ModelForm):
    class Meta:
        model = Softwarerental
        fields = ['softwarestock','people', 'place', 'count', 'bigo']
        widgets = {
            'softwarestock': forms.HiddenInput
        }