from django import forms
from .models import Category


CHOICES = [('', '----')] + [category for category in Category.objects.all().values_list('name', 'name')]


class ListingForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    image = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'placeholder' : 'Url for image(optional)'
    }))
    category = forms.ChoiceField(required=False, choices=CHOICES)


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class BidForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)