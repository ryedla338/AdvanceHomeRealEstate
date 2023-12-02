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
    price_range_span = models.CharField(max_length=50)

    def __str__(self):
        return self.price_range_span


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
    price_range = models.ForeignKey(PropertyPriceRange, on_delete=models.DO_NOTHING)
    neighborhood = models.ForeignKey(PropertyNeighborhood, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
