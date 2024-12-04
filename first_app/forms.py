from django import forms 

class FormName(forms.Form):
    Review = forms.CharField(widget=forms.Textarea)

class MovieSearchForm(forms.Form):
    Search = forms.CharField(max_length=200)


class ResturantSearchForm(forms.Form):
    Search = forms.CharField(max_length=200)

class RestaurantLocSearchForm(forms.Form):
    Location = forms.CharField(max_length=200)