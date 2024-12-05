
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete-transaction/<id>/', views.delete_transaction, name="delete_transaction"),
    path('log-in/',views.login_view,name="login_view"),
    path('registration/',views.registration_view,name="registration_view"),
    path('log-out/',views.logout_view,name="logout_view"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        
urlpatterns += staticfiles_urlpatterns()