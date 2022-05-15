from pydoc import describe
from turtle import update
from venv import create
from django.db import models 
from django.contrib.auth.models import User 
from django.core.validators import MaxValueValidator, MinValueValidator 
STATE_CHOICES=( 
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'), 
	('Andhra Pradesh', 'Andhra Pradesh'), 
	('Arunachal Pradesh', 'Arunachal Pradesh'), 
	('Assam', 'Assam'), 
	('Bihar', 'Bihar'), 
	('Chandigarh', 'Chandigarh'), 
	('Chhattisgarh', 'Chhattisgarh'), 
	('Dadra & Nagar Haveli', 'Dadra & Nagar Haveli'), 
	('Daman and Diu', 'Daman and Diu'), 
	('Delhi', 'Delhi'), 
	('Goa', 'Goa'), 
	('Gujarat', 'Gujarat'), 
	('Haryana', 'Haryana'), 
	('Himachal Pradesh', 'Himachal Pradesh'), 
	('Jammu & Kashmir', 'Jammu & Kashmir'), 
	('Jharkhand', 'Jharkhand'), 
	('Karnataka', 'Karnataka'), 
	('Kerala', 'Kerala'), 
	('Lakshadweep', 'Lakshadweep'), 
	('Madhya Pradesh', 'Madhya Pradesh'), 
	('Maharashtra', 'Maharashtra'), 
	('Manipur', 'Manipur'), 
	('Meghalaya', 'Meghalaya'), 
	('Mizoram', 'Mizoram'), 
	('Nagaland', 'Nagaland'), 
	('Odisha', 'Odisha'), 
	('Puducherry', 'Puducherry'), 
	('Punjab', 'Punjab'), 
	('Rajasthan', 'Rajasthan'),
	('Sikkim', 'Sikkim'),
	('Tamil Nadu', 'Tamil Nadu'),
	('Telangana', 'Telangana'),
	('Tripura', 'Tripura'),
	('Uttarkhand', 'Uttarkhand'),
	('Uttar Pradesh', 'Uttar Pradesh'),
	('West Bengal', 'West Bengal'),
)

class Customer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES, max_length=500)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES=(
     ('M', 'Mobile'),
     ('L', 'Laptop'),
     ('TW', 'Top Wear'),
     ('BW', 'Bottom Wear'),
     ('GE', 'Gym'),
     ('HA', 'House Appliances'),
     ('MS', 'Medical Store'),
     ('RM', 'Raw Materials'),
     ('TS', 'Toys'),
     ('PD', 'PinDrives'),
     ('FD', 'Fridge'),
     ('KB', 'Keyboard'),
     ('PE', 'Printer'),
     ('CL', 'Cooler'),
     ('TB', 'Teddy'),
     ('BC', 'Cycle'),
     ('TT', 'Train'),
     ('PT', 'Plain'),
     ('BT', 'Barbie'),
     ('DT', 'Doll'),
     ('BJ', 'Bangles'),
     ('EJ', 'Ear-Rings'),
     ('NJ', 'Necklace'),
     ('RJ', 'Rings'),
     ('JB','Bracelets'),
     ('BR','Broaches'),
     ('NP','Nose Pin'),
     ('JCH','Chains'),
     ('BPP','Belly Pins'),
     ('BRR','Briyani'),
     ('PZZ','Pizza'),
     ('CHH','Chinees'),
     ('DSS','Desserts'),
     ('MSS','Meals'),
     ('TFS','Tiffins'),
     ('SSS','Sarees'),
     ('WSS','Western'),
     ('KTS','Kurtis'),
     ('ETS','Ethnic'), 
     ('STS','Suits'),  
     ('PUS','Purses'), 
     ('TTS','T-Shirts'),
     ('SST','Shirts'),
     ('JNS','Jeans'),
     ('NTS','Night Suits'),     
     ('ACC','Accessroies'),
     ('PTW','Party Wear'),
     ('BYS','Boy Set'),
     ('GRS','Girl Set'),
     ('SEW','Ethnic Wear'),
     ('SNW','Night Wear'),
     ('WTW','Winter Wear'),
     ('FTW','Foot Wear'),
     ('STs','Sprots'),
     ('FTS','Fruits'),
     ('VTS','Vegetables'),
     ('MSL','Masalas'),
     ('EGG','Egg'),
     ('FGS','Food Grains'),
     ('OIL','Oils'),
     ('MET','Meat'),
     ('FSH','Fish'),
     ('BVS','Beverages'),
     ('SKS','Snaks'), ## 
     ('GSD','Shoulder Press'),
     ('GCP','Chest Press'),
     ('GLP','Lats Pull Down'),
     ('GBM','Biceps Curl Machine'),
     ('GTM','Triceps Curl Machine'),
     ('GDM','Dumbbell'),
     ('GRS','Rods'),
     ('Bars','bars'),
     ('GALM','All Rounds Machines'), ##     
     ('Beds','Beds'),
     ('SofaSets','Sofa Sets'),
     ('ArmChair','Arm Chair'),
     ('Tables','Tables'),
     ('BookCases','Book Cases'),
     ('Cupboards','Cupboards'), ##
     ('Stoves','Stoves'),
     ('LightBulbs','Light Bulbs'),
     ('Fans','Fans'),
     ('Blenders','Blenders'),
     ('Mixers','Mixers'),
     ('Ovens','Ovens'),
     ('VaccumCleaners','Vaccum Cleaners'),
     ('WashineMachines','Washine Machines'),
     ('RiceCookers','Rice Cookers'),
     ('PressureCookers','Pressure Cookers'),
     ('WaterPurifiers','Water Purifiers'), ##     
     ('Corns','Corns'),
     ('Gasoline','Gasoline'),
     ('Plastic','Plastic'),
     ('Lumber','Lumber'),
     ('Forest','Forest'),
     ('Mineral','Mineral'),
     ('Natural','Natural'),
     ('Coal','Coal'),
     ('Steel','Steel'), ##
     ('Syrups','Syrups'),
     ('Tablets','Tablets'),
     ('Ointments','Ointments'),
     ('Drops','Drops'),
     ('Injections','Injections'),
     ('Bandages','Bandages'), ##
    ('monitors', 'Monitors'), 
    ('computers', 'Computers'), 
    ('printers' , 'Printers'), 
    ('speakers', 'Speakers'),
    ('ACs',  'ACs'), 
    ('coolers', 'Coolers'), 
    ('fridges', 'Fridges '),
    ('television ', 'Television '),
    ('dVDs',  'DVDs'), 
    ('cameras',  'Cameras'), 
    ('watches',  'Watches')
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices= CATEGORY_CHOICES,max_length=500)
    product_image=models.ImageField(upload_to='producting')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price    


STATUS_CHOICES=(
  ('Accepted', 'Accepted'),
  ('Packed', 'Packed'),
  ('On The Way', 'On The Way'),
  ('Delivered', 'Delivered'),
  ('Cancel', 'Cancel')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, choices= STATUS_CHOICES, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price 
    

WORK_CHOICES=(
    ('Plumber','Plumber'),
    ('Electrician','Electrician'),
    ('Carpentry','Carpentry'),
    ('Welder','Welder'),
    ('Saloon','Saloon'),
    ('Tailor','Tailor'),
)

class HomeServices(models.Model):
    name = models.CharField(max_length=126)
    profile = models.ImageField(upload_to='homeServices')
    mobile = models.CharField(max_length=12)
    address = models.CharField(max_length=126)
    category=models.CharField(choices= WORK_CHOICES,max_length=120)
    experience = models.IntegerField(max_length=12)
    proof = models.ImageField(upload_to='homeServices')

    def __str__(self):
        return str(self.id)

class HomeServicesOrder(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(HomeServices, on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, choices= STATUS_CHOICES, default='Pending')        

class ServicesCart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    services=models.ForeignKey(HomeServices, on_delete=models.CASCADE)
    date = models.CharField(max_length=26)
    days = models.IntegerField(max_length=12)
    hours = models.IntegerField(max_length=12)
    
    def __str__(self):
        return str(self.id)

# Hotel Room Bookings
HOTEL_CHOICES=(
    ('single','Single Room'),
    ('double','Double Room'),
    ('5 Star Deluex','5 Star Deluex'),
    ('Family Type Room','Family Type Room'),
    ('Studio Room','Studio Room'),
)

class HotelRooms(models.Model):
    name = models.CharField(max_length=126)
    room = models.ImageField(upload_to='hotelRooms')
    mobile = models.CharField(max_length=12)
    address = models.CharField(max_length=126)
    description=models.TextField()
    category=models.CharField(choices= HOTEL_CHOICES,max_length=120)

    def __str__(self):
        return str(self.id)

class HotelRoomsOrder(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(HotelRooms, on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, choices= STATUS_CHOICES, default='Pending')        

class RoomsCart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    services=models.ForeignKey(HotelRooms, on_delete=models.CASCADE)
    date = models.CharField(max_length=26)
    days = models.IntegerField(max_length=12)
    
    def __str__(self):
        return str(self.id)

# Train Bookings
TYPE_CHOICES = (
    ('AC','AC'),
    ('NON-AC','NON-AC'),
)


class TrainDetail(models.Model):
    trainName = models.CharField(max_length=220)
    trainNumber = models.IntegerField()
    fromCity = models.CharField(choices=STATE_CHOICES, max_length=500)
    toCity = models.CharField(choices=STATE_CHOICES, max_length=500)
    seat_type = models.CharField(choices=TYPE_CHOICES, max_length=500)
    availableOn = models.DateField()
    destinationTime = models.CharField(max_length=120)
    arrivalTime = models.CharField(max_length=120)
    distance = models.IntegerField()
    amount = models.IntegerField()                
    image = models.ImageField(upload_to='trainDetails')

    def __str__(self):
        return str(self.trainName)

class TrainBooked(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(TrainDetail, on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, choices= STATUS_CHOICES, default='Pending')   


class BookedCart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    services=models.ForeignKey(TrainDetail, on_delete=models.CASCADE)
    passengers = models.IntegerField()          

# Movie Tickets
LANGUAGE_CHOICES = (
    ('Hindi','Hindi'),
    ('Telugu','Telugu'),
)

TYPE_CHOICES = (
    ('Thriller','Thriller'),
)

class Movie(models.Model):
    name = models.CharField(max_length=120)
    movieLanguage = models.CharField(choices=LANGUAGE_CHOICES, max_length=120)
    movieType = models.CharField(choices=TYPE_CHOICES, max_length=120)
    duration = models.CharField(max_length=120)
    cast = models.CharField(max_length=200)
    directorName = models.CharField(max_length=200)
    releaseDate = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to='movies')

    def __str__(self):
        return self.name

# Flight
class FlightDetail(models.Model):
    trainName = models.CharField(max_length=220)
    trainNumber = models.IntegerField()
    fromCity = models.CharField(choices=STATE_CHOICES, max_length=500)
    toCity = models.CharField(choices=STATE_CHOICES, max_length=500)
    availableOn = models.DateField()
    destinationTime = models.CharField(max_length=120)
    arrivalTime = models.CharField(max_length=120)
    amount = models.IntegerField()                
    image = models.ImageField(upload_to='trainDetails')

    def __str__(self):
        return str(self.trainName)

class FlightBooked(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(FlightDetail, on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, choices= STATUS_CHOICES, default='Pending')   


class FlightCart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    services=models.ForeignKey(FlightDetail, on_delete=models.CASCADE)
    passengers = models.IntegerField()          
        
# Bus
TYPE_CHOICES = (
    ('AC','AC'),
    ('NON-AC','NON-AC'),
)


class BusDetail(models.Model):
    trainName = models.CharField(max_length=220)
    trainNumber = models.CharField(max_length=20)
    fromCity = models.CharField(choices=STATE_CHOICES, max_length=500)
    toCity = models.CharField(choices=STATE_CHOICES, max_length=500)
    seat_type = models.CharField(choices=TYPE_CHOICES, max_length=500)
    availableOn = models.DateField()
    destinationTime = models.CharField(max_length=120)
    arrivalTime = models.CharField(max_length=120)
    distance = models.IntegerField()
    amount = models.IntegerField()                
    image = models.ImageField(upload_to='busDetails')

    def __str__(self):
        return str(self.trainName)

class BusBooked(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(BusDetail, on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50, choices= STATUS_CHOICES, default='Pending')   


class BusCart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    services=models.ForeignKey(BusDetail, on_delete=models.CASCADE)
    passengers = models.IntegerField()          
        