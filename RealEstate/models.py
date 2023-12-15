from django.db import models
from django.utils import timezone


class Owner(models.Model):
    name = models.CharField(max_length=25)
    photo = models.ImageField(upload_to='owner/')
    office_address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email_id = models.EmailField()

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class PropertyPriceRange(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PropertyNeighborhood(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class OmahaEvent(models.Model):
    omaha_event_id = models.IntegerField(primary_key=True)
    omaha_event_title = models.CharField(max_length=255)
    omaha_event_url = models.TextField()
    omaha_event_description = models.CharField(max_length=150)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.omaha_event_title


class PropertyListing(models.Model):
    name = models.CharField(max_length=30, default=None)
    description = models.CharField(max_length=150)
    price = models.IntegerField()
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=60)
    zipcode = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=[
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold')
    ], max_length=10, default='available')

    featured = models.BooleanField(default=False)
    photo1 = models.ImageField(upload_to='listing_images/')
    photo2 = models.ImageField(upload_to='listing_images/', blank=True)
    photo3 = models.ImageField(upload_to='listing_images/', blank=True)
    photo4 = models.ImageField(upload_to='listing_images/', blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.DO_NOTHING)
    property_type = models.ForeignKey(PropertyType, on_delete=models.DO_NOTHING)
    property_price_range = models.ForeignKey(PropertyPriceRange, on_delete=models.DO_NOTHING)
    neighborhood = models.ForeignKey(PropertyNeighborhood, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):

        if self.featured:

            PropertyListing.objects.exclude(pk=self.pk).update(featured=False)

        super(PropertyListing, self).save(*args, **kwargs)

    def toggle_featured(self):
        if not self.featured:
            self.featured = True
            self.save()

    def __str__(self):
        return self.name




class Search(models.Model):
    neighborhood = models.ForeignKey(PropertyNeighborhood, on_delete=models.DO_NOTHING, null=True, blank=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.DO_NOTHING, null=True, blank=True)
    property_price_range = models.ForeignKey(PropertyPriceRange, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        search_str = f"Search ID: {self.id} - "
        filters = []

        if self.neighborhood:
            filters.append(f"Neighborhood: {self.neighborhood.name}")

        if self.property_type:
            filters.append(f"Property Type: {self.property_type.name}")

        if self.property_price_range:
            filters.append(f"Price Range: {self.property_price_range.name}")

        return search_str + ", ".join(filters)