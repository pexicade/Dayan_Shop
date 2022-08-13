from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Province, City, Address
from .forms import CustomUserChangeForm, CustomUserCreationForm, AddressForm

class CustomUserAdmin(UserAdmin):
    model = User
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = (
        "email","first_name","last_name","is_active"
    )

    fieldsets = (
        ('Account info', {
            "fields": ("email","password")
        }),
        ('Persnoal info',{
            "fields": ('first_name', 'last_name', 'phonenumber', 'birthdate')
        }),
        ('Body info',{
            "fields": ('bodytype', 'height', 'weight')
        }),
        ('Address', {
            'fields': ('address', )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'address','is_staff', 'is_active')}
        ),
    )
    ordering = ('date_joined','email')

class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    # province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities', blank=False)
    list_display = (
        "city","date_created"
    )

    fieldsets = (
        ('Address', {
            'fields': ('province', 'city', 'address', 'postal_code')
        }),
    )

    ordering = ['date_created', 'city']

    class Media:
        js = ('https://code.jquery.com/jquery-3.6.0.min.js','CustomUser/js/updateCityListAdmin.js')    

class CityInline(admin.TabularInline):
    model = City

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    inlines = [CityInline]

# admin.site.register(User, CustomUserAdmin)
# admin.site.register(Province,ProvinceAdmin)
# admin.site.register(City,CityAdmin)
# admin.site.register(Address, AddressAdmin)