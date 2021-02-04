from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.LoginView.as_view()),
    path('admin/', admin.site.urls),
    path('gshs/', include('gshs.urls')),  
    path('accounts/', include('accountapp.urls')),
    path('memo/', include('memo.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG: 
#     import debug_toolbar 
#     urlpatterns += [ path('__debug__/', include(debug_toolbar.urls)), ]

