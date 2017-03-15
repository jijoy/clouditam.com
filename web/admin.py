from django.contrib import admin
from web.models import Header, Customer, Account, Setting, Feature, Demo, Client, About, Contact

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True

    def has_delete_permission(self, request, obj=None):
        return False if self.model.objects.count() <= 1 else True

    def get_actions(self, request):
        actions = super(HeaderAdmin,self).get_actions(request)
        if (self.model.objects.count() <= 1):
            del actions['delete_selected']
        return actions

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'phone_number', 'plan_name', 'asset_limit', 'price', 'type', 'assets_count')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(CustomerAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_limit', 'price', 'price_detail', 'color_code', 'type')
    list_display_links = ('name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_display_links = ('name',)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True

    def has_delete_permission(self, request, obj=None):
        return False if self.model.objects.count() <= 1 else True

    def get_actions(self, request):
        actions = super(AboutAdmin, self).get_actions(request)
        if (self.model.objects.count() <= 1):
            del actions['delete_selected']
        return actions

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True

    def has_delete_permission(self, request, obj=None):
        return False if self.model.objects.count() <= 1 else True

    def get_actions(self, request):
        actions = super(ContactAdmin, self).get_actions(request)
        if (self.model.objects.count() <= 1):
            del actions['delete_selected']
        return actions



@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True

    def has_delete_permission(self, request, obj=None):
        return False if self.model.objects.count() <= 1 else True

    def get_actions(self, request):
        actions = super(SettingsAdmin, self).get_actions(request)
        if (self.model.objects.count() <= 1):
            del actions['delete_selected']
        return actions

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('icon','title','text')
    list_display_links = ('title',)

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 5 else True

@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    list_display = ('title','text')
    list_display_links = ('title',)

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 2 else True