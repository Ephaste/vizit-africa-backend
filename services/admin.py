from django.contrib import admin
from .models import Service, ServiceMedia, ServiceAvailability, Discount
# Register your models here.


admin.site.register(Service)
admin.site.register(ServiceMedia)
admin.site.register(ServiceAvailability)
admin.site.register(Discount)