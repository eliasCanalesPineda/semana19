from django import forms

class Add_prod(forms.Form):
    nombre=forms.CharField(max_length=100)
    stock=forms.IntegerField()
    fk_prov=forms.IntegerField()