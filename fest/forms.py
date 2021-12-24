from django import forms
class PayPage(forms.Form): 
    
    Name = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={"class": "form-control"})) 
    
    Club = forms.CharField(widget = forms.TextInput(attrs={"class": "form-control"})) 
    Event = forms.CharField(widget = forms.TextInput(attrs={"class": "form-control",'readonly': 'readonly'})) 
    Fee = forms.CharField(widget = forms.TextInput(attrs={"class": "form-control",'readonly': 'readonly'})) 
    