from django.db import models
from datetime import datetime 
from django.core.exceptions import ValidationError
from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse


class Infogigi(models.Model):
    productgubun = models.ForeignKey("gshs.Productgubun", on_delete=models.CASCADE, null=True, blank=True)
    buy_date = models.DateField(blank=True, null=True)
    people = models.ForeignKey("gshs.People", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to = {'status': True})
    place = models.ForeignKey("gshs.Place", on_delete=models.CASCADE, null=True, blank=True)    
    maker = models.CharField(max_length=50)
    model = models.CharField(max_length=100)  
    color_choices = (
        ('흑백', '흑백'),
        ('컬러', '컬러'),
    )  
    color = models.CharField(max_length=6, choices=color_choices, null=True, blank=True)    
    ip = models.CharField(max_length=20, blank=True, null=True)  
    status = models.BooleanField(default=True)  
    bigo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['productgubun','buy_date']
        db_table = 'infogigi'

    def __str__(self):
        return '{}'.format( self.model)

class Place(models.Model):
    building = models.CharField(max_length=50, null=True, blank=True)
    room = models.CharField(max_length=50, default=0, null=False, blank=True)
    buseo_choices = (
        ('부서', '부서'),
        ('강의실', '강의실'),
        ('강당', '강당'),
        ('실험실', '실험실'),
        ('기타', '기타'),
    )
    buseo = models.CharField(max_length=30, choices=buseo_choices)
    bigo = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['building']
        db_table = 'place'

    def __str__(self):
        return '({}) {}'.format(self.building, self.room)

class People(models.Model):
    name = models.CharField(u'성명', max_length=100, null=True, blank=True)    
    phone_number = models.CharField(u'핸드폰', max_length=20, blank=True, null=True)
    tel_number = models.CharField(u'내선', max_length=5, blank=True, null=True)
    status = models.BooleanField('재직', default=True)
    bigo = models.CharField('비고', max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['name']
        db_table = 'people'

    def __str__(self):
        return '{}'.format(self.name)

class Jaego(models.Model):
    created_date = models.DateField(auto_now_add=True)    
    infogigi = models.ForeignKey("gshs.Infogigi", on_delete=models.SET_NULL, null=True)
    rental_choices = (
        ('yes', '가능'),
        ('no', '대여중'),
    )
    rental_status = models.CharField(max_length=3, choices=rental_choices, default='yes', null=False, blank=True)
    not_use = models.BooleanField(default=False)
    bigo = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['-rental_status']
        db_table = 'jaego'

    def __str__(self):
        return '{}'.format(self.infogigi)

class Gigirental(models.Model):
    rental_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    jaego = models.ForeignKey("gshs.Jaego", on_delete=models.CASCADE, blank=True)
    people = models.ForeignKey("gshs.People", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to = {'status': True})
    place = models.ForeignKey("gshs.Place", on_delete=models.CASCADE, null=True, blank=True)
    bigo = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['-rental_date']
        db_table = 'gigirental'

    def __str__(self):
        return '{}'.format(self.rental_date)

    def get_absolute_url(self):
        return reverse('gshs:gigirental_list')

class Repair(models.Model):
    created_date = models.DateField(auto_now_add=True)
    infogigi = models.ForeignKey("gshs.Infogigi", on_delete=models.SET_NULL, null=True, blank=True)
    place = models.ForeignKey("gshs.Place", on_delete=models.SET_NULL, null=True, blank=True)
    cause = models.CharField(max_length=200)
    result = models.TextField()      
    price = models.PositiveIntegerField(default=0, null=False, blank=True)
    bigo = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['-created_date']
        db_table = 'repair'

    def __str__(self):
        return '[{}] {}'.format(self.cause, self.result)

    def get_absolute_url(self):
        return reverse('gshs:suri_list')
    

class Productbuy(models.Model):
    created_date = models.DateField(auto_now_add=True)
    productgubun = models.ForeignKey("gshs.Productgubun", on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey("gshs.Vendor", on_delete=models.CASCADE, null=True, blank=True)
    maker = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=100)
    count = models.PositiveSmallIntegerField(default=1, blank=True)
    price = models.PositiveIntegerField(default=0, null=False, blank=True)
    bigo = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['productgubun', 'model']
        db_table = 'productbuy'

    def __str__(self):
        return '{}'.format(self.model)

class Vendor(models.Model):
    created_date = models.DateField(auto_now_add=True)
    company = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    damdang_name = models.CharField(max_length=20, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    bigo = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['company']
        db_table = 'vendor'

    def __str__(self):
        return f'{self.company}'


class Bupumchange(models.Model):
    created_date = models.DateField(auto_now_add=True)
    infogigi = models.ForeignKey("gshs.Infogigi", on_delete=models.SET_NULL, null=True, blank=True)
    productbuy = models.ForeignKey("gshs.Productbuy", on_delete=models.SET_NULL, null=True)
    count = models.PositiveSmallIntegerField(default=1, null=False, blank=True)
    price = models.PositiveIntegerField(default=0, null=False, blank=True)
    bigo = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['-created_date']
        db_table = 'bupumchange'

    # def __str__(self):
    #     return '{}'.format(self.productbuy)
class Productgubun(models.Model):
    table_name = models.CharField(max_length=30, default='infogigi')
    gubun_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'productgubun'

    def __str__(self):
        return '{} / {}'.format(self.table_name,self.gubun_name)

def file_size(value): 
    limit = 3 * 1024 * 1024 
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MB.')

class Photo(models.Model):
    suri = models.ForeignKey("gshs.Repair", on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey("gshs.Place", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(validators=[file_size], upload_to = "images/%Y/%m", null=False, blank=True) 

    class Meta:
        db_table = 'photo'

    # def delete(self, *args, **kargs):
    #     if not self.image:
    #         self.__class__.objects.delete()
    #     super().delete(*args, **kargs)

class Softwarestock(models.Model):
    created_date = models.DateField(auto_now_add=True)
    model = models.CharField(max_length=100)
    count = models.PositiveSmallIntegerField(default=1, blank=True)
    price = models.PositiveIntegerField(default=0, null=False, blank=True) 
    remain = models.PositiveSmallIntegerField(null=True, blank=True) 

    class Meta:
        db_table = 'softwarestock'

    def __str__(self):
        return '{}'.format(self.model)

    # @property
    # def remaining2(self):
    #     if self.remaining is not None:
    #         return self.remaining
    #     return self.productbuy.count
    
class Softwarerental(models.Model):
    rental_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    softwarestock = models.ForeignKey("gshs.Softwarestock", on_delete=models.CASCADE, null=False, blank=True)    
    people = models.ForeignKey("gshs.People", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to = {'status': True})
    place = models.ForeignKey("gshs.Place", on_delete=models.CASCADE, null=True, blank=True)
    count = models.PositiveSmallIntegerField(default=1, blank=True, help_text='남은 수량 보다 많이 입력하지마세요.!')
    bigo = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['-rental_date']
        db_table = 'softwarerental'