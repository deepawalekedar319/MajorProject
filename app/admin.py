from django.contrib import admin
from .models import (
    BookedCart,
    BusBooked,
    BusCart,
    BusDetail,
    Customer,
    FlightBooked,
    FlightCart,
    FlightDetail,
    HomeServices,
    HotelRooms,
    HotelRoomsOrder,
    Movie,
    Product,
    Cart,
    OrderPlaced,
    HomeServicesOrder,
    RoomsCart,
    # Seat,
    ServicesCart,
    TrainBooked,
    TrainDetail
)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']
    search_fields = ['title', 'brand']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'product', 'quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']


@admin.register(HomeServices)
class HomeServicesAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'address', 'mobile', 'category', 'experience', 'proof']

@admin.register(HomeServicesOrder)
class HomeOrderAdmin(admin.ModelAdmin):
    list_display=['id','user','customer']

@admin.register(ServicesCart)
class HomeCartAdmin(admin.ModelAdmin):
    list_display=['id','user','services']    
    
admin.site.register(HotelRooms)
admin.site.register(HotelRoomsOrder)
admin.site.register(RoomsCart)      
admin.site.register(Movie)
admin.site.register(TrainDetail)
admin.site.register(TrainBooked)
admin.site.register(BookedCart)
admin.site.register(FlightBooked)
admin.site.register(FlightDetail)
admin.site.register(FlightCart)
admin.site.register(BusDetail)
admin.site.register(BusBooked)
admin.site.register(BusCart)