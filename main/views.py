from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CarListing, Specification, Feature, CarImage, Wishlist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Register View
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Automatically log in after registration
        return redirect('index')  # Redirect to the home page

    return render(request, 'register.html')


# Login View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email exists in the database
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            # Authenticate the user using the email and password
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to homepage or desired page
            else:
                messages.error(request, 'Invalid password. Please try again.')
                return render(request, 'login.html', {'error': True})
        else:
            messages.error(request, 'No user found with that email address.')
            return render(request, 'login.html', {'error': True})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    brand = request.GET.get('brand', '')
    if brand:
        cars = CarListing.objects.filter(car_name__icontains=brand)
    else:
        cars = CarListing.objects.all()

    return render(request, 'index.html', {'cars': cars})


from django.shortcuts import render
from .models import CarListing

def add_car(request):
    if request.method == 'POST':
        # Create the car listing object with main car image
        car_listing = CarListing(
            user=request.user,
            car_name=request.POST['car_name'],
            car_image=request.FILES['car_image'],  # main car image
            price=request.POST['price'],
            model=request.POST['model'],
            year=request.POST['year'],
            color=request.POST['color'],
            kilometers=request.POST['kilometers'],
            owner=request.POST['owner'],
            fuel_type=request.POST['fuel_type'],
            transmission=request.POST['transmission'],
            engine=request.POST['engine'],
            insurance_validity=request.POST['insurance_validity']
        )
        car_listing.save()

        # Handle selected specifications
        specifications = request.POST.getlist('specifications')
        for spec_name in specifications:
            specification, created = Specification.objects.get_or_create(name=spec_name)
            car_listing.specifications.add(specification)

        # Handle selected features
        features = request.POST.getlist('features')
        for feature_name in features:
            feature, created = Feature.objects.get_or_create(name=feature_name)
            car_listing.features.add(feature)

        # Handle additional images
        additional_images = request.FILES.getlist('additional_images')
        for image in additional_images:
            # Create a CarImage instance for each additional image
            CarImage.objects.create(car=car_listing, image=image)

        return redirect('your_listings')  # Redirect to your listings page or any success page

    return render(request, 'add_car.html')

def delete_car(request, id):
    listing = get_object_or_404(CarListing, id=id)
    if listing.user == request.user:  # Ensure the user is the owner of the listing
        listing.delete()
    return redirect('your_listings')

def your_listings(request):
    listings = CarListing.objects.filter(user=request.user)
    return render(request, 'your_listing.html', {'listings': listings})

def view_details(request, id):
    # Fetch the car listing based on the provided ID
    car_listing = get_object_or_404(CarListing, id=id)
    
    # Render the details page and pass the car listing object
    return render(request, 'car_details.html', {'car_listing': car_listing})

def car_details(request, car_id):
    car = CarListing.objects.get(id=car_id)
    in_wishlist = Wishlist.objects.filter(user=request.user, car=car).exists()
    
    # Get specifications and features
    specifications = car.specifications.all()  # Add this line
    features = car.features.all()  # Add this line

    if request.method == 'POST':
        if in_wishlist:
            Wishlist.objects.filter(user=request.user, car=car).delete()
        else:
            Wishlist.objects.create(user=request.user, car=car)
        return redirect('car_details', car_id=car.id)

    return render(request, 'car_details.html', {
        'car': car,
        'in_wishlist': in_wishlist,
        'specifications': specifications,  # Add this line
        'features': features,  # Add this line
    })


@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(CarListing, id=car_id)
    
    # Check if the car is already in the wishlist
    if not Wishlist.objects.filter(user=request.user, car=car).exists():
        Wishlist.objects.create(user=request.user, car=car)

    return redirect('car_details', car_id=car.id)

def your_wishlist(request):
    if request.method == 'POST':
        # Check if 'car_id' is in the POST data to remove the car
        car_id = request.POST.get('car_id')
        if car_id:
            car = CarListing.objects.get(id=car_id)
            # Remove the car from the user's wishlist
            Wishlist.objects.filter(user=request.user, car=car).delete()
        return redirect('your_wishlist')  # Redirect to the same page after removal

    # Fetch all wishlist items for the current user
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'your_wishlist.html', {
        'wishlist_items': wishlist_items,
    })

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CarListing, Wishlist

def car_details(request, car_id):
    try:
        car = CarListing.objects.get(id=car_id)
    except CarListing.DoesNotExist:
        return HttpResponse("Car not found.", status=404)
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the car is already in the user's wishlist
        in_wishlist = Wishlist.objects.filter(user=request.user, car=car).exists()
        
        if request.method == 'POST':
            # Add to wishlist if not already in the wishlist
            if not in_wishlist:
                Wishlist.objects.create(user=request.user, car=car)
                in_wishlist = True  # Update the variable after adding
    else:
        in_wishlist = False

    # Get the features and specifications
    features = car.features.all()
    specifications = car.specifications.all()

    return render(
        request,
        'car_details.html',
        {
            'car': car,
            'in_wishlist': in_wishlist,
            'features': features,
            'specifications': specifications
        }
    )
