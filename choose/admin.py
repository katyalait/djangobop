from django.contrib import admin

#add the model to let superuser touch it
from .models import User_Image
from .models import Colour
from .models import Result

admin.site.register(User_Image)
admin.site.register(Colour)
admin.site.register(Result)
