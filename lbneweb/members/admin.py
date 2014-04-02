from django.contrib import admin
from members.models import Role, Institution, Individual

class IndividualAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'roles')
    list_filter = ('role','institution')
    list_per_page = 500
    ordering = ('last_name', 'first_name')

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'country', 'number_of_members')
    list_filter = ('country',)
    ordering = ('sort_name',)
    
admin.site.register(Role)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Individual, IndividualAdmin)

