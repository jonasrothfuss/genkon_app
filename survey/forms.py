from django import forms
from .models import Profile

"""
class ProfileDataForm(forms.Form):
    first_name = forms.CharField(label='Vorname ', max_length=30)
    last_name = forms.CharField(label='Nachname ', max_length=50)
    email = forms.EmailField(label='E-Mail')
    phone_number = forms.CharField(label='Telefonnummer', max_length=20, required=False)
    occupation = forms.CharField(label='Beruf', max_length=40)
    street = forms.CharField(label='Adresse', max_length=40)
    zip_code = forms.CharField(label='PLZ', max_length=10)
    city =  forms.CharField(label='Wohnort', max_length=40)
    message = forms.CharField(widget=forms.Textarea, label='Nachricht', max_length=1000, required=False)
"""

class ProfileDataForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['date_posted']