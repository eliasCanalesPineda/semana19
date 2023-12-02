from django import forms
class Add_prov(forms.Form):
    nombre=forms.CharField(max_length=100)
    telefono=forms.CharField(max_length=8)