from typing import Any, Optional
from django import forms
from .models import SENTINELLE
from .models import Laboratoire
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.validators import RegexValidator
import openpyxl
from .models import CustomUser
import pycountry
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django_countries.widgets import CountrySelectWidget

User = get_user_model()

# Every letter to LowerCase
class Lowercase(forms.CharField):
    def to_python(self, value):
        return value.lower()

# Every letter to UpperCase
class Uppercase(forms.CharField):
    def to_python(self, value):
        return value.upper()

class ImportExcelForm(forms.Form):
    fichier_excel = forms.FileField(label='Charger un Fichier Excel')

class MonFormulaire(forms.Form):
    fichier_excel = forms.FileField()


class SENTINELLEForm(forms.ModelForm): 
    Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = SENTINELLE
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        user_country = kwargs.pop('user_country', None)
        super().__init__(*args, **kwargs)
        if user_country:
            self.fields['Sites_sentinelles'].queryset = Laboratoire.objects.filter(country=user_country)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['institution', 'last_name', 'first_name', 'email', 'country']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'form-control'})



class PasswordDefineForm(SetPasswordForm):
    """
    Form for defining a user's password.
    """
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].label = "New password"
        self.fields['new_password2'].label = "New password confirmation"




class PasswordChangeForm(DjangoPasswordChangeForm):
    old_password = forms.CharField(
        label="Ancien mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="""
            Votre mot de passe doit contenir au moins 8 caractères.
            Il ne doit pas être trop similaire à vos autres informations personnelles.
            Il ne doit pas être un mot de passe couramment utilisé.
            Il doit être unique par rapport aux autres mots de passe que vous avez déjà utilisés.
        """,
    )
    new_password2 = forms.CharField(
        label="Confirmation du nouveau mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                "L'ancien mot de passe saisi est incorrect."
            )
        return old_password

class CustomForm(forms.Form):
    country = forms.CharField(widget=CountrySelectWidget)






















            # Validations
    
    #IRA=forms.CharField (
       # label='Infections Respiratoires aiguës', min_length=1, max_length=3,
       # validators= [RegexValidator(r'^[0-9]*$',
       # message="only Number is allowed !")],
      #  widget= forms.TextInput()
   # )
    
    #Suspect_COVID=forms.CharField (
       #label='Nombre de cas Suspects de COVID-19', min_length=1, max_length=3,
       # validators= [RegexValidator(r'^[0-9]*$',
       # message="only Number is allowed !")],
       # widget= forms.TextInput()
  # )
    
    
   # Cas_Preleves=forms.CharField (
        #label='Nombre de cas prélevés', min_length=1, max_length=3,
       # validators= [RegexValidator(r'^[0-9]*$',
       # message="only Number is allowed !")],
      #  widget= forms.TextInput()
  #  )

  #  Cas_Positif_Covid=forms.CharField (
     ##   label='Nombre de Cas positifs de COVID-19', min_length=1, max_length=3,
     #   validators= [RegexValidator(r'^[0-9]*$',
     #   message="only Number is allowed !")],
     #   widget= forms.TextInput()
   # )
    #Cas_Positif_Influenza=forms.CharField (
     #  label='Nombres de Cas Positifs Influenza B', min_length=1, max_length=3,
     #   validators= [RegexValidator(r'^[0-9]*$',
      #  message="only Number is allowed !")],
      #  widget= forms.TextInput()
   #)

   # Cas_Positif_Autres_virus=forms.CharField (
      #  label='Nombres de Cas Positifs Autres Virus Respiratoire', min_length=1, max_length=3,
     #   validators= [RegexValidator(r'^[0-9]*$',
     #   message="only Number is allowed !")],
     #   widget= forms.TextInput()
   # )
  #  Cas_Positif_RSV=forms.CharField (
       # label='Nombres de Cas Positifs RSV', min_length=1, max_length=3,
       # validators= [RegexValidator(r'^[0-9]*$',
       # message="only Number is allowed !")],
       # widget= forms.TextInput()
   # )

   # IRA_Positif_Covid=forms.CharField (
      #  label='Nombre d IRA positifs de COVID-19', min_length=1, max_length=3,
      #  validators= [RegexValidator(r'^[0-9]*$',
       # message="only Number is allowed !")],
      #  widget= forms.TextInput()
   # )
   # Deces_covid=forms.CharField (
       # label='Nombre de decès dus à COVID-19', min_length=1, max_length=3,
      #  validators= [RegexValidator(r'^[0-9]*$',
      #  message="only Number is allowed !")],
      #  widget= forms.TextInput()
  # )
  #  Deces_covid=forms.CharField (
    #    label='Nombre de decès dus à COVID-19', min_length=1, max_length=3,
     #   validators= [RegexValidator(r'^[0-9]*$',
     #   message="only Number is allowed !")],
     #   widget= forms.TextInput()

    
  #  )
   # Deces_IRA_covid=forms.CharField (
       # label='Nombre de decès par IRA et  COVID-19', min_length=1, max_length=3,
       # validators= [RegexValidator(r'^[0-9]*$',
       # message="only Number is allowed !")],
       # widget= forms.TextInput()
   # )
