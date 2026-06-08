from django.contrib import admin

from .models import Food

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'address', 'note')
