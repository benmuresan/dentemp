from django.contrib import admin
from dentemp_site.models import UserProfile, OfficeProfile, EventProfile, DateAvailable


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(UserProfile)
admin.site.register(OfficeProfile)
admin.site.register(EventProfile)
admin.site.register(DateAvailable)