from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import openpyxl
import pandas as pd
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pycountry
import phonenumbers
from django import forms
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


#import rpy2.robjects as robjects
##from rpy2.robjects import pandas2ri



GROUPE=[('< 5 ans', '< 5 ans'), ('5-15 ans', '5-15 ans'),
  ('15-50 ans', '15-50 ans'),('50 ans et plus', '50 ans et plus'),('Age manquant', 'Age manquant')]

SEX_CHOICES = [('HOMME ', 'HOMME'), ('FEMME', 'FEMME')]

STATUS = [('Tous','Tous'),('Totalement', 'Totalement'),
          ('Partiellement ','Partiellement '),
          ('Pas Vacciné', 'Pas Vacciné'),('Aucun', 'Aucun') ]
TYPES_SITES = [('Hopitalier', 'Hopitalier'),('Communautaire', 'Communautaire'),('Laboratoire ', 'Laboratoire')]

INSTITUT_CHOICES=[ 
        ('Centre Pasteur du Cameroun', 'Centre Pasteur du Cameroun'),
        ('Institut Pasteur de Bangui (IPB)', 'Institut Pasteur de Bangui (IPB)'),
        ('Institut Pasteur de Dakar (IPD)', 'Institut Pasteur de Dakar (IPD)'),
        ('Institut Pasteur de Madagascar (IPM)', 'Institut Pasteur de Madagascar (IPM)'),
        ('Institut de Recherche Clinique du Bénin (IRCB)', 'Institut de Recherche Clinique du Bénin (IRCB)'),
        ('Institut Pasteur de Côte  Ivoire', 'Institut Pasteur de Côte  Ivoire'),
        ('Institut Pasteur de Guinée','Institut Pasteur de Guinée'),
        ('Institut commémoratif Noguchi pour la recherche médicale  Accra (NMIMR)','Institut commémoratif Noguchi pour la recherche médicale Accra (NMIMR)'),
        ('Institut National de Santé Publique Ouagadougou (INSP)','Institut National de Santé Publique Ouagadougou (INSP)'),
        ('CERMES Niamey ','CERMES Niamey'),
        ('Institut National de Santé Publique Bamako (INSP)','Institut National de Santé Publique Bamako (INSP)'),
        ('Institut National de Recherche Biomédicale Kinshasa (INRB)','Institut National de Recherche Biomédicale Kinshasa (INRB)'),
        ('Laboratoire de Biologie Moléculaire et d’Immunologie Lomé (BIOLIM)','Laboratoire de Biologie Moléculaire et d’Immunologie Lomé (BIOLIM)'),
        
        ]




# Create your models here.


class COUNTRY(models.Model):
    name = models.CharField(max_length=100)
   

    def __str__(self):
        return self.name

class Laboratoire(models.Model):
    nom = models.CharField(max_length=100)
    country = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, null=True, blank=True)
    Sites_sentinelles = models.CharField(max_length=100)
    def __str__(self):
        return self.nom
    
    #pays = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, null=True, blank=True)
    
class SENTINELLE(models.Model):
    
    Date=models.DateField(auto_now_add=False,auto_now=False,blank=True,)
    Type_de_Site=models.CharField(max_length=25,choices=TYPES_SITES)
    Nombre_IRA_Syndrômme_gripaux= models.CharField(max_length=100, blank= True )
    IRA=models.CharField(max_length=100, blank= True )
    Suspect_COVID=models.CharField(max_length=100, blank=True )
    Hospitalisation=models.CharField(max_length=100, blank=True )
    Cas_Preleves=models.CharField(max_length=100,blank=True)
    Cas_Positif_Covid=models.CharField(max_length=100,blank=True)
    Cas_Positif_Influenza=models.CharField(max_length=100,blank=True)
    Cas_Positif_Autres_virus=models.CharField(max_length=100,blank=True)
    Cas_Positif_RSV=models.CharField(max_length=100,blank=True)
    IRA_Positif_Covid=models.CharField(max_length=100,blank=True)
    Deces_covid=models.CharField(max_length=100, blank=True)
    Deces_IRA_covid=models.CharField(max_length=100, blank=True)
    Sexe=models.CharField(max_length=15,choices=SEX_CHOICES)
    Groupe_age=models.CharField(max_length=100, choices=GROUPE)
    nombre_de_Consultation=models.CharField(max_length=100, blank= True)
    Statut_Vaccinal=models.CharField(max_length=100, choices=STATUS,)
    Sites_sentinelles=models.ForeignKey(Laboratoire, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, null=True, blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("can_view_data_for_country", "Peut voir les données pour son pays", ),
        )

    def __str__(self):
        return self.Sites_sentinelles
    
    

class CustomUser(AbstractUser):
    # Utilisez l'e-mail comme nom d'utilisateur
    username = models.EmailField(_('email address'), unique=True)

    groups = models.ManyToManyField(Group, related_name='sites_sentinelles_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_permissions')
    institution = models.CharField(max_length=200, choices=INSTITUT_CHOICES)
   # country = CountryField()
    country = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, null=True, blank=True)
   

    STATUS_CHOICES = [
        ('Activated', 'Activated'),
        ('Deactivated', 'Deactivated'),
        ('Rejected', 'Rejected'),
        ('Pending Approval', 'Pending Approval'),
    ]
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, default='Deactivated')
    token_expiration_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email
    















#country = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, limit_choices_to={'country__in': CountryField().countries}, null=True, blank=True, related_name='users')
#country = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, null=True, blank=True)
    #country = CountryField(blank=True, null=True)

#COUNTRY_CHOICES = [(country.name, country.name) for country in pycountry.countries]
    #country = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, limit_choices_to={'name__in': [choice[0] for choice in COUNTRY_CHOICES]}, null=True, blank=True, related_name='users')   



















'''
class CustomUser(AbstractUser):
    
    country = models.ForeignKey(COUNTRY, on_delete=models.CASCADE, null=True, blank=True, related_name='users')   
    groups = models.ManyToManyField(Group, related_name='sites_sentinelles_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_permissions')

    def __str__(self):
        return self.username
    



class Registration(models.Model):
    institution = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    
    pays_choices = [(country.name, country.name) for country in pycountry.countries]
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),]
    
    adresse_mail = models.EmailField(max_length=254)
    pays = models.CharField(max_length=100, choices=pays_choices)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, default='Pending')
    token_expiration_date = models.DateTimeField(blank=True, null=True)

   

    @property
    def all_countries(self):
       
        return [country.name for country in pycountry.countries]'''










































def importer_fichier_excel(fichier):
    # Enregistrer le fichier dans le stockage par défaut de Django
    chemin_fichier = default_storage.save(fichier.name, ContentFile(fichier.read()))

    return True
###============================== Fonction pour importer un fichier excel et le tester avec pandas  =============================

def importer_fichier_excel(fichier):
    data_frame = pd.read_excel(fichier)

    for index, row in data_frame.iterrows():
        PAYS = row['PAYS']
        SITE = row['Sites sentinelles']
        Type_site = row['Type de site']
        MOIS = row['MOIS']
        effectif_total = row['Effectif total']
        sexe_homme = row['Homme']
        sexe_femme = row['Femme']
        moins_de_5_ans_homme = row['<5ans Homme']
        moins_de_5_ans_femme = row['<5ans Femme']
        entre_5_et_15_ans_homme = row['5-15 ans Homme']
        entre_5_et_15_ans_femme = row['5-15 ans Femme']
        entre_15_et_50_ans_homme = row['15-50 ans Homme']
        entre_15_et_50_ans_femme = row['15-50 ans Femme']
        plus_de_50_ans_homme = row['50 ans et plus Homme']
        plus_de_50_ans_femme = row['50 ans et plus Femme']
        age_manquant_homme = row['Age manquant Homme']
        age_manquant_femme = row['Age manquant Femme']
        statut_vaccinal_partiellement = row['Statut Vaccinal Partiellement vacciné']
        statut_vaccinal_totalement = row['Statut Vaccinal Totalement vacciné']
        statut_vaccinal_non_vaccine = row['Statut Vaccinal Non vacciné']
        statut_vaccinal_inconnu = row['Statut Vaccinal Inconnu']

        # code pour traiter les données récupérées

        

    return True

    


