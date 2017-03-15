from django.contrib import admin

# Register your models here.
from dashboard.models import *
from web.models import Customer


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    readonly_fields = ('asset_tag','id')
    list_display = ('asset_tag', 'assigned_to', 'serial','status', 'model', 'supplier', 'location', 'purchase_cost', 'order_number', 'purchase_date', 'name')
    list_display_links = ('asset_tag',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
            actions = super(AssetAdmin, self).get_actions(request)
            del actions['delete_selected']
            return actions

    # def save_model(self, request, obj, form, change):
    #     obj.save()
    #
    #     cats = dict(CATEGORY_TYPES)
    #     obj.asset_tag = "{0}{1:04d}{2:05d}".format({cats[k]: k for k in cats}[obj.model.get_category_display()],
    #                                                request.user.customer.id, obj.id)
    #     obj.save()
    #     request.user.customer.assets.add(obj)

@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ('model', 'manufacturer', 'category')
    list_display_links = ('model',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(HardwareAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ManufacturerAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(CompanyAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'location_currency', 'address', 'city', 'state', 'postal_code', 'country')
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(LocationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'phone_number', 'fax_number', 'email', 'url', 'address', 'city', 'state', 'postal_code', 'country')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(SupplierAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'licensed_to_name', 'licensed_to_email', 'seats', 'assigned_to', 'is_os', 'reassignable', 'maintained', 'supplier', 'purchase_date')
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(SoftwareAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

@admin.register(DashUser)
class DashUserAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'city', 'state', 'postal_code', 'country', 'phone_number', 'email')
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(DashUserAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions





