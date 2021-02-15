from django.urls import path
from gshs import views


app_name = 'gshs'
urlpatterns = [
    path('infogigi/gigi/<str:gigigubun>/', views.InfogigiLV.as_view(), name='infogigi_list'),
    path('infogigi/update/<int:pk>/', views.update_infogigi, name='update_infogigi'),
    path('infogigi/delete/<int:pk>/', views.delete_infogigi, name='delete_infogigi'),    
    path('infogigi/create/', views.create_infogigi, name='create_infogigi'), 
    path('infogigi/search/', views.SearchinfoLV.as_view(), name='search_infogigi'),
    path('infogigi/export-excel/', views.export_excel, name='export_excel'),
    #수리
    path('infogigi/suri/list/', views.RepairLV.as_view(), name='suri_list'),
    path('infogigi/suri/', views.suri_infogigi, name='suri_infogigi'),    
    path('infogigi/suri/search', views.SearchRepairLV.as_view(), name='search_suri'),    
    path('infogigi/suri/<int:pk>/', views.RepairPhotoUV.as_view(), name='suri_update'),
    path('infogigi/suri/delete/<int:pk>/', views.suri_delete, name='suri_delete'),
    # productbuy
    path('infogigi/productbuy/', views.ProductbuyLV.as_view(), name='productbuy_list'),
    path('infogigi/productbuy/search', views.SearchProductBuyLV.as_view(), name='search_productbuy'),
    path('infogigi/productbuy/create/', views.create_productbuy, name='create_productbuy'),
    path('infogigi/productbuy/update/<int:pk>/', views.update_productbuy, name='update_productbuy'),
    path('infogigi/productbuy/delete/<int:pk>/', views.delete_productbuy, name='delete_productbuy'),
    #재고
    path('infogigi/jaego/', views.JaegoLV.as_view(), name='jaego_list'),
    path('infogigi/jaego/search', views.SearchJaegoLV.as_view(), name='search_jaego'),
    path('infogigi/jaego/<int:pk>/', views.jaego_infogigi, name='jaego_infogigi'),  
    path('infogigi/jaego/rental/', views.jaego_rental, name='jaego_rental'),  
    #기기렌탈 
    path('infogigi/gigirental/', views.GigirentalLV.as_view(), name='gigirental_list'), 
    path('infogigi/gigirental/receive/<int:pk>/', views.gigirental_receive, name='gigirental_receive'), 
    path('infogigi/gigirental/delete/<int:pk>/', views.gigirental_delete, name='gigirental_delete'), 
    #widget
    path('infogigi/widget/productgubun/', views.productgubun_select, name='productgubun_select'),     
    #People
    path('infogigi/people/', views.PeopleLV.as_view(), name='people_list'),
    path('infogigi/people/search/', views.SearchpeopleLV.as_view(), name='search_people'),
    path('infogigi/people/create/', views.PeopleCV.as_view(), name='create_people'),
    path('infogigi/people/update/<int:pk>/', views.PeopleUV.as_view(), name='update_people'),
    path('infogigi/people/delete/<int:pk>/', views.delete_people, name='people_delete'),
    # 소프트웨어 재고
    path('infogigi/softwarestock/', views.SoftwarestockLV.as_view(), name='softwarestock_list'),
    path('infogigi/softwarestock/rental/', views.software_rental, name='software_rental'),
    # 소프트웨어 렌탈
    path('infogigi/softwarerental/', views.SoftwarerentalLV.as_view(), name='softwarerental_list'),
    path('infogigi/softwarerental/receive/<int:pk>/', views.softwarerental_receive, name='softwarerental_receive'), 
    #부품 교환
    path('infogigi/bupum/list/', views.BupumLV.as_view(), name='bupum_list'),
    path('infogigi/bupum/change/', views.bupum_infogigi, name='bupum_infogigi'), 
    path('infogigi/bupum/search/', views.SearchbupumLV.as_view(), name='search_bupum'),
    path('infogigi/bupum/update/<int:pk>/', views.update_bupum, name='update_bupum'),
    path('infogigi/bupum/delete/<int:pk>/', views.delete_bupum, name='delete_bupum'),
    # 위치
    path('infogigi/place/list/<str:buseo_gubun>/', views.PlaceLV.as_view(), name='list_place'),
] 
  
