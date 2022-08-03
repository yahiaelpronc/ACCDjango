from re import A
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Myuser)
admin.site.register(Vet)
admin.site.register(locations)
admin.site.register(Messages)
admin.site.register(Animal)
admin.site.register(Medication)
admin.site.register(SurgicalOperationsRequest)
admin.site.register(SurgicalOperations)
admin.site.register(ServiseRequest)
admin.site.register(Notifications)
