from django.contrib import admin
from members.models import Role, Institution, Individual

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name','desc', 'number_of_individuals')
    ordering = ('name',)

class IndividualAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'roles')
    list_filter = ('role','institution')
    list_per_page = 1000
    ordering = ('last_name', 'first_name')

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'country', 'number_of_members')
    list_filter = ('country',)
    ordering = ('sort_name',)
    list_per_page = 1000
    
admin.site.register(Role, RoleAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Individual, IndividualAdmin)

