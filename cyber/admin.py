from django.contrib import admin
from .models import User, Content, Course, Quiz, Email

# Register your models here.

admin.site.register(User)
admin.site.register(Content)
admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(Email)
