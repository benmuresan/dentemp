from django.contrib import admin
from dentemp_site.models import UserProfile, OfficeProfile, EventProfile, DateAvailable

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OfficeProfile)
admin.site.register(EventProfile)
admin.site.register(DateAvailable)
