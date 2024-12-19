from django.contrib import admin

# Register your models here.
from .models import Specification, Feature, CarListing, CarImage, Wishlist

class CarListingAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'model', 'price', 'year', 'color', 'kilometers', 'owner', 'fuel_type', 'transmission')
    search_fields = ('car_name', 'model', 'owner')
    list_filter = ('fuel_type', 'transmission', 'year', 'color')
    filter_horizontal = ('specifications', 'features')
    date_hierarchy = 'insurance_validity'

class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'image')
    search_fields = ('car__car_name',)  # Allow search by car name

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'car')
    search_fields = ('user__username', 'car__car_name')

class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register your models
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(CarListing, CarListingAdmin)
admin.site.register(CarImage, CarImageAdmin)
admin.site.register(Wishlist, WishlistAdmin)
