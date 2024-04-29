"""SITE_SENTINELLES URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sites_sentinelles import views
from SITE_SENTINELLES import settings


from django.conf.urls.static import static
from django.contrib.auth import views as auth_views





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('home/', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('backend', views.backend, name='backend'),
    path('reject_user_account/<int:registration_id>/', views.reject_user_account, name='reject_user_account'),
    path('recapitulatif/', views.recapitulatif, name='recapitulatif'),
     path('change_password/', views.change_password, name='change_password'),
    path('password_define/<uidb64>/<token>/', views.password_define, name='password_define'),
    path('confirm-and-send-email/<int:registration_id>/',  views.confirm_and_send_email, name='confirm_and_send_email'),
    
    
    #path('verifier/', views.verifier, name='verifier'),
   # path('run_verification_scrip', views.run_verification_scrip, name='charger_fichier_excel'),
    path('charger_fichier_excel', views.charger_fichier_excel, name='charger_fichier_excel'), #######
    path('register', views.register, name='register'),
    path('<int:id>/', views.edit, name='edit'),
    path('sentinelles/<int:sentinelle_id>/delete', views.data_delete, name='data_delete'),
    
    
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)