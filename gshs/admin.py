from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Infogigi)
class InfogigiAdmin(ImportExportModelAdmin):
    list_display = ('buy_date', 'productgubun','people', 'place', 'maker', 'model', 'color', 'ip', 'status', 'bigo')
    raw_id_fields = ['people']
    list_filter = ['buy_date']
    search_fields = ['people__name', 'place__room']

@admin.register(Jaego)
class JaegoAdmin(ImportExportModelAdmin):
    list_display = ('created_date','infogigi', 'rental_status', 'not_use', 'bigo')

class PhotoInline(admin.StackedInline):
    model = Photo

# class FileInline(admin.StackedInline):
#     model=File

@admin.register(Gigirental)
class GigirentalAdmin(admin.ModelAdmin):
    list_display = ('rental_date','due_date', 'jaego', 'people', 'place', 'bigo')

@admin.register(Repair)
class RepairAdmin(ImportExportModelAdmin):
    list_display = ('created_date', 'infogigi', 'cause', 'result', 'price', 'bigo')    
    inlines = (PhotoInline,)

@admin.register(Place)
class PlaceAdmin(ImportExportModelAdmin):
    list_display = ('building', 'room', 'buseo', 'bigo')   
    inlines = (PhotoInline,)

@admin.register(Productbuy)
class ProductbuyAdmin(admin.ModelAdmin):
    list_display = ('productgubun','vendor', 'maker', 'model', 'count', 'price', 'bigo')
 #manytomantField 일 경우 자료 표현을 위해...
    # def get_vendors(self, obj):
    #     return "\n".join([p.company for p in obj.vendor.all()])

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('company', 'address', 'damdang_name', 'tel', 'bigo')

@admin.register(Bupumchange)  
class BupumchangeAdmin(admin.ModelAdmin):
    list_display = ('infogigi', 'productbuy', 'count', 'price', 'bigo')

@admin.register(People)
class PeopleAdmin(ImportExportModelAdmin):
    list_display = ('name', 'tel_number', 'status', 'bigo')


@admin.register(Productgubun)
class ProductgubunAdmin(admin.ModelAdmin):
    list_display = ('gubun_name',)

@admin.register(Softwarestock)
class SoftwarestockAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'model', 'count', 'price', 'remain')

@admin.register(Softwarerental)
class SoftwarestockAdmin(admin.ModelAdmin):
    list_display = ('rental_date', 'softwarestock','people', 'place', 'count', 'bigo')