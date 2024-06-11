from django.contrib import admin

from boxes.models import Memory, Box


# Register your models here.
@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'creator', 'date_created', 'date_opening', 'status', 'category')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'box', 'content_type', 'description')
    prepopulated_fields = {'slug': ('name',)}