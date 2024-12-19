from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Specification(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class CarListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Link to User model
    car_name = models.CharField(max_length=100)
    car_image = models.ImageField(upload_to='car_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    kilometers = models.PositiveIntegerField()
    owner = models.CharField(max_length=20)
    fuel_type = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20)
    engine = models.CharField(max_length=50)
    insurance_validity = models.DateField()
    
    # Many-to-many relationships for specifications and features
    specifications = models.ManyToManyField(Specification, blank=True)
    features = models.ManyToManyField(Feature, blank=True)

    def __str__(self):
        return self.car_name

class CarImage(models.Model):
    car = models.ForeignKey(CarListing, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return f"Image of {self.car.car_name}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    car = models.ForeignKey(CarListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.car.car_name}"