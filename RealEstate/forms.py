from django import forms
from .models import PropertyListing


class PropertyListingForm(forms.ModelForm):
    class Meta:
        model = PropertyListing
        fields = ('name', 'owner', 'street', 'city', 'state', 'zipcode', 'price', 'price_range',
                 'description', 'neighborhood', 'photo1', 'photo2', 'photo3', 'photo4', 'status', 'featured')
