from django.core.paginator import Paginator
import os
from uuid import uuid4
import subprocess
import rpy2.robjects as robjects
import subprocess
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth import get_user_model
from .forms import SENTINELLEForm
from .models import SENTINELLE, Laboratoire, COUNTRY, CustomUser
from django.http import HttpResponseRedirect
from django.contrib import messages
import openpyxl
import pandas as pd
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import ImportExcelForm
from .models import importer_fichier_excel
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views import View
from django.http import HttpResponse
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from datetime import datetime
from .utils import send_email_with_html_body
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist  # Importez cette classe d'exception
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_decode
import six
from .forms import PasswordDefineForm
import logging
from django.http import HttpResponseRedirect
#from django.views.decorators.cache import never_cache

# Configurez le logging
logger = logging.getLogger(__name__)








#=================LOGIN==================== |
@login_required(login_url="login")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def home(request):
    return render (request, "home.html")
    
# ===================SENTINELLE IMPORTER FICHIER EXCEL=============

def charger_fichier_excel(request):
    if request.method == 'POST':
        # Traitement du formulaire ici...
        return HttpResponse("Le fichier a été chargé avec succès.")
    else:
        form = ImportExcelForm()
        context = {'form': form, 'button_test': True}
        return render(request, 'charger_fichier_excel.html', context)


def excel_verification(chemin_fichier):
    excel_sheets = pd.ExcelFile(chemin_fichier).sheet_names
    data_frame_forresult = pd.DataFrame({"Sheet": [""], "etat": [""], "error": [""]})

    for i, sheet_name in enumerate(excel_sheets, start=1):
        df = pd.read_excel(chemin_fichier, sheet_name)
        resultat_verification = verifie_template(df, int(df.iloc[0, 8]))

        if not resultat_verification:
            etat = False
            error = f"Dans la feuille N°{i}: {resultat_verification}"
        else:
            etat = resultat_verification
            error = None

        temp_data=pd.DataFrame({"Sheet": [f"Sheet {i}"], "etat": [etat], "error": [error]})
        data_frame_forresult = pd.concat([data_frame_forresult, temp_data], axis=0, ignore_index=True)
        
    data_frame_forresult=data_frame_forresult.loc[data_frame_forresult['Sheet']!=""]
    return data_frame_forresult

def verifie_template(df, id_temp):
    test_country = df.iloc[0, 1] in ["Madagascar", "Senegal", "Central African Republic"]
    test_site = df.iloc[1, 1] in ["CHU ANOSIALA", "CENHOSOA", "CHUJRB", "CHU AMITIE"]
    test_type_of_site = df.iloc[2, 1] in ["Hospitalier", "Communautaire"]    
    test_date_report =  df.iloc[3,1] in ["01","02","03","04","05"]  

    return all([test_country, test_site, test_type_of_site, test_date_report])


#================  Login page =====================|
def login(request):
    return render (request, "login.html")
# ===================SENTINELLE REGISTRATION   (both create and update)=============| Egalité

def register(request):
    user_country = request.user.country
    if request.method == "POST":
        form = SENTINELLEForm(request.POST, user_country=request.user.country)
        
        if form.is_valid():
            sentinelle = form.save(commit=False)
            sentinelle.user = request.user # Si vous voulez enregistrer l'utilisateur qui a créé l'enregistrement
            # Pré-remplir la liste déroulante des laboratoires avec ceux associés au pays de l'utilisateur connecté
            sentinelle.Sites_sentinelles = form.cleaned_data['Sites_sentinelles']
            sentinelle.save()
            messages.success(request, "Enregistré avec succès !")
            return redirect('/register')
        else:
            messages.error(request, "Erreur lors de l'enregistrement.")
    else:
        form = SENTINELLEForm()
        # Pré-remplir la liste déroulante des laboratoires avec ceux associés au pays de l'utilisateur connecté
        laboratories = Laboratoire.objects.filter(country=user_country)
        form.fields['Sites_sentinelles'].queryset = laboratories
    return render(request, "register.html", {'form': form})

def data_delete(request, sentinelle_id):
    if request.method == 'POST':
        sentinelle = get_object_or_404(SENTINELLE, id=sentinelle_id)
        sentinelle.delete()
        return redirect('/backend')
    else:
        return HttpResponseRedirect('/backend')
#=================BACKEND ==================== |
def backend(request):
    user_country = request.user.country
    if request.user.is_superuser:
        # Vue pour l'administrateur qui affiche les données de tous les pays 
        all_sentinelles_list = SENTINELLE.objects.all().order_by('-created_at')
    else:
        # Vue pour l'utilisateur qui affiche les données de son propre pays 
        all_sentinelles_list = SENTINELLE.objects.filter(Sites_sentinelles__country=user_country).order_by('-created_at')
        
    paginator = Paginator(all_sentinelles_list, 200)
    page = request.GET.get('page')
    all_sentinelle = paginator.get_page(page)
    context = {'sentinelles': all_sentinelle}
    return render(request, "backend.html", context)

#=================Function to edit =====================|

def edit(request, id=None):
    user_country = request.user.country
    if request.method == "POST":
        if id is None:
            form = SENTINELLEForm(request.POST, user_country=request.user.country)
        else:
            sentinelle = SENTINELLE.objects.get(pk=id)
            form = SENTINELLEForm(request.POST, instance=sentinelle)
        if form.is_valid():
            form.save()
            messages.success(request, "Mise à jour réussie !")
            return redirect('/register')
        else:
            messages.error(request, "Erreur lors de la mise à jour.")
    else:
        if id is None:
            form = SENTINELLEForm()
        else:
            sentinelle = SENTINELLE.objects.get(pk=id)
            form = SENTINELLEForm(instance=sentinelle)
        # Pré-remplir la liste déroulante des laboratoires avec ceux associés au pays de l'utilisateur connecté
        laboratories = Laboratoire.objects.filter(country=user_country)
        form.fields['Sites_sentinelles'].queryset = laboratories
        return render(request, "edit.html", {'form': form})



def recapitulatif(request):
    
    registrations = CustomUser.objects.all()
    return render(request, "recapitulatif.html", {'registrations': registrations})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  # Récupérer l'e-mail à partir du formulaire
            first_name = form.cleaned_data['first_name'] 
            last_name=form.cleaned_data['last_name']
            try:
                existing_user = CustomUser.objects.get(username=email)  # Vérifier si un utilisateur avec cette adresse e-mail existe déjà
                # Gérer le cas où l'utilisateur existe déjà (par exemple, afficher un message d'erreur)
                # ...  
            except ObjectDoesNotExist:
                new_registration = form.save(commit=False)
                new_registration.username = email  # Utiliser l'e-mail comme nom d'utilisateur
                new_registration.save()



                subject = "Bienvenue sur la plateforme EWS-AFROSCREEN"
                template = 'registration_email.html'
                context = {
                'date': datetime.today().date,
                'email': email,
                'first_name':first_name,
                'last_name':last_name
                }
                
                receivers = [email]
            
                # Envoyer l'e-mail
                has_send = send_email_with_html_body(subject, receivers, template, context)

                # Reste du code pour envoyer l'e-mail et afficher le formulaire
                # ...
                form = RegistrationForm()  # nouvelle instance de formulaire vide
                return render(request, 'registration_form.html', {'form': form})
    else:
        form = RegistrationForm()

    return render(request, 'registration_form.html', {'form': form})


def confirm_and_send_email(request, registration_id):
    registration = get_object_or_404(CustomUser, id=registration_id)

    # Générer le token et l'URL pour définir le mot de passe
    user = CustomUser.objects.filter(email=registration.email).first()
    if user:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        define_password_url = f"http://127.0.0.1:8000/password_define/{uid}/{token}/"
        
        

        # Envoyer l'e-mail avec le lien pour définir le mot de passe
        subject = "Bienvenue sur la plateforme EWS-AFROSCREEN"
        context = {
            'define_password_url': define_password_url,
            'expiration_date': timezone.now() + timedelta(days=3),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date': datetime.today().date()
        }
        template = 'define_password_email.html'
        html_content = render_to_string(template, context)
        
        text_content = "Bienvenue sur la plateforme EWS-AFROSCREEN. Veuillez suivre le lien ci-dessous pour définir votre mot de passe."

        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        user.statut = 'Pending Approval'
        user.save()
        
    else:
        messages.error(request, "Utilisateur non trouvé")

    return render(request, 'recapitulatif.html')




def password_define(request, uidb64, token):
    try:
        # Décodage de l'UID
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = CustomUser.objects.get(pk=uid)

        # Vérification du token
        if not default_token_generator.check_token(user, token):
            logger.error(f'Token invalide ou expiré pour l\'utilisateur {user.pk}')
            return HttpResponse('Le lien de réinitialisation du mot de passe est invalide ou a expiré.')

        # Traitement de la requête
        if request.method == 'GET':
            form = PasswordDefineForm(user, request.POST or None)
            return render(request, 'password_define.html', {'form': form})
        elif request.method == 'POST':
            form = PasswordDefineForm(user, request.POST or None)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                
                # Mettre à jour le statut de l'utilisateur à "Activated"
                user.statut = 'Activated'
                
                user.save()
                logger.info(f'Mot de passe défini avec succès pour l\'utilisateur {user.pk}')
                return HttpResponse('Mot de passe défini avec succès')
            else:
                return render(request, 'password_define.html', {'form': form})

    except CustomUser.DoesNotExist:
        logger.error('Tentative de réinitialisation de mot de passe pour un utilisateur inexistant')
        return HttpResponse('Le lien de réinitialisation du mot de passe est invalide ou a expiré.')
    except Exception as e:
        logger.exception('Erreur inattendue lors de la définition du mot de passe')
        return HttpResponse('Une erreur inattendue est survenue.')
    
    
def reject_user_account(request, registration_id):
    registration = get_object_or_404(CustomUser, id=registration_id)
    user = CustomUser.objects.filter(email=registration.email).first()
    if user:
    # Envoyer l'e-mail pour informer l'utilisateur que sa demande de creation de compte n'a pas ete accepte 
        subject = "Bienvenue sur la plateforme EWS-AFROSCREEN"
        context = {
            
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date': datetime.today().date()
        }
        template = 'reject.html'
        html_content = render_to_string(template, context)
        
        text_content = "Bienvenue sur la plateforme EWS-AFROSCREEN."

        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        user.statut = 'Rejected'
        user.save()
        
    else:
        messages.error(request, "Utilisateur non trouvé")

    return render(request, 'recapitulatif.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            return redirect('change_password')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })










# vue pour confirmation et l'envoie des emails a un utilisateur 
'''def confirm_and_send_email(request, customuser_id):
    customuser_id = CustomUser.objects.get(id=customuser_id)  # Remplacez "Registration" par le nom de votre modèle d'inscription
    if customuser_id.statut == 'Approved':
        # Généreration du token avec une validité de 7 jours
        token = default_token_generator.make_token(User.objects.get(email=customuser_id.adresse_mail))

        customuser_id.token_expiration_date = timezone.now() + timezone.timedelta(days=7)
        customuser_id.save()
        
        #  lien pour la définition des paramètres
        token_link = f"http://127.0.0.1:8000/pasword_define/?token={token}"
        
        # contenu de l'e-mail
        subject = "Définissez votre nom d'utilisateur et votre mot de passe"
        message = render_to_string('confirmation_email.html', {'token_link': token_link})
        #sender = "your@example.com"
        receiver = registration.adresse_mail
        
        # Envoi l'e-mail
        send_mail(subject, message, [receiver])
        
    return render(request, 'recapitulatif.html')   # Redirigons  l'utilisateur vers une page de confirmation'''




'''
def password_define(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            confirm_password = form.cleaned_data.get('password2')
            
            # Vérifier si les mots de passe correspondent
            if password != confirm_password:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return redirect('password_define')
            
            # Créer un nouvel utilisateur
            user = User.objects.create_user(username=username, password=password)
            user.save()
            
            messages.success(request, f"Le compte pour {username} a été créé avec succès !")
            return redirect('login')  # Rediriger vers la page de connexion
    else:
        form = UserCreationForm()
    return render(request, 'password_define.html', {'form': form})

'''


# vue qui permet de faire une demande de creation de compte et l'envoi de mail 


'''def registration(request):
   
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_registration = form.save(commit=False)
            email = new_registration.email  # Récupérer l'e-mail à partir du formulaire
            
            new_registration.save()
            
            # Préparation du  contenu de l'e-mail
            subject = "Bienvenue sur la plateforme EWS-AFROSCREEN"
            template = 'registration_email.html'
            context = {
            'date': datetime.today().date,
            'email': email
             }
            
            receivers = [email]
            
            # Envoyer l'e-mail
            has_send = send_email_with_html_body(subject, receivers, template, context)


            
           
            form = RegistrationForm()  # nouvelle instance de formulaire vide
            return render(request, 'registration_form.html', {'form': form})
    else:
        form = RegistrationForm()
    
    return render(request, 'registration_form.html', {'form': form})'''



'''def password_define(request, uidb64, token):
    try:
        uid = six.text_type(urlsafe_base64_decode(uidb64), 'utf-8')
       
        user = CustomUser.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == 'GET':
                form = PasswordDefineForm()
                return render(request, 'password_define.html', {'form': form})
            elif request.method == 'POST':
                form = PasswordDefineForm(request.POST)
                if form.is_valid():
                    # Logique pour gérer la soumission du formulaire pour définir le mot de passe
                    new_password = form.cleaned_data['new_password1']
                    user.set_password(new_password)
                    user.save()
                    return HttpResponse('Mot de passe défini avec succès')
                else:
                    return render(request, 'password_define.html', {'form': form})
        else:
            return HttpResponse('Le lien de réinitialisation du mot de passe est invalide ou a expiré.')
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return HttpResponse('Le lien de réinitialisation du mot de passe est invalide ou a expiré.')'''