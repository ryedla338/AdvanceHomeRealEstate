from django import forms
from .models import PropertyListing, PropertyType, PropertyNeighborhood, PropertyPriceRange, Search


class PropertyListingForm(forms.ModelForm):
    class Meta:
        model = PropertyListing
        exclude = []
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }


class PropertyListingEditForm(forms.ModelForm):
    class Meta:
        model = PropertyListing
        fields = ['name', 'description', 'price', 'street', 'city', 'state', 'zipcode', 'status', 'featured', 'photo1',
                  'photo2', 'photo3', 'photo4', 'owner', 'property_type', 'property_price_range', 'neighborhood']


from django import forms

class TypeSearchForm(forms.ModelForm):
    property_type = forms.ModelChoiceField(
        empty_label="Select Home Type        ",
        queryset=PropertyType.objects.all(),  # Replace with your actual model
        widget=forms.Select(attrs={'class': 'form-control'}),
        required = False
    )

    class Meta:
        model = Search
        fields = ("property_type",)


class NeighborhoodSearchForm(forms.ModelForm):
    neighborhood = forms.ModelChoiceField(
        empty_label="Select Neighborhood",
        queryset=PropertyNeighborhood.objects.all(),  # Replace with your actual model
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Search
        fields = ("neighborhood",)


class PriceSearchForm(forms.ModelForm):
    property_price_range = forms.ModelChoiceField(
        empty_label="Select Price ",
        queryset=PropertyPriceRange.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Search
        fields = ("property_price_range",)

