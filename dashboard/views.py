from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from dashboard.forms import AssetForm, CompanyForm, ManufacturerForm, SupplierForm, SoftwareForm, DashUserForm, \
    HardwareForm, LocationForm, AccountForm
from dashboard.models import CATEGORY_TYPES, Asset, Software, DashUser, Supplier, Manufacturer, Location, Company, \
    Hardware
from web.models import Account
from django.contrib import messages


class DashboardView(View):
    template_name = 'dashboard/index.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)


class AccountSettingsView(View):
    template_name = 'dashboard/account-settings.html'
    form_class = AccountForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(instance=request.user.customer)
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.customer)
        if form.is_valid():
            obj = form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            message = 'Account settings updated.'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('account-settings')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class SubscriptionView(View):
    template_name = 'dashboard/subscription.html'

    @method_decorator(login_required)
    def get(self, request):
        plans = Account.objects.all().exclude(name=request.user.customer.plan_name, type=request.user.customer.type).exclude(type="Free")
        context = {"plans": plans}
        return render(request, self.template_name, context)


class AssetsView(View):
    template_name = 'dashboard/assets.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)


class AssetShowView(View):
    template_name = 'dashboard/layouts/asset_show.html'

    @method_decorator(login_required)
    def get(self, request, tag):
        obj = get_object_or_404(Asset, asset_tag=tag, customer=request.user.customer)
        # logs = LogEntry.objects.filter(object_id=obj.id, content_type__id__exact=ContentType.objects.get_for_model(Asset).id)
        logs = obj.history.all().order_by('-timestamp')
        context = {"asset": obj, "history": logs, "softwares": Software.objects.filter(customer=request.user.customer)}
        return render(request, self.template_name, context)

class AssetDuplicateView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to duplicate asset. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('assets')
        obj = get_object_or_404(Asset, id=id_obj, customer=request.user.customer)
        try:
            clone = obj.clone()
        except AttributeError:
            message = 'Cannot duplicated. Reason: Asset doesn\'t have model. Please edit asset first.'
            messages.add_message(request, messages.ERROR, message)
            return redirect('assets')
        # f_l = clone.fullname.split('-')
        # try:
        #     clone.fullname = f_l[0] + '-' + str(int(f_l[1])+1)
        # except IndexError:
        #     clone.fullname = clone.fullname + '-' + str(1)
        # clone.save()
        cats = dict(CATEGORY_TYPES)
        clone.asset_tag = "{0}{1:04d}{2:05d}".format({cats[k]: k for k in cats}[clone.model.get_category_display()],
                                                   request.user.customer.id, clone.id)
        clone.save()
        request.user.customer.assets.add(clone)
        message = 'Asset "{0}" successfully duplicated.'.format(clone.asset_tag)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('assets')


class AssetDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Asset, id=id_obj, customer=request.user.customer)
        obj.delete()
        message = 'Asset "{0}" successfully deleted.'.format(obj.asset_tag)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('assets')


class AssetEditView(View):
    template_name = 'dashboard/layouts/asset_edit.html'
    form_class = AssetForm

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Asset, id=id_obj, customer=request.user.customer)
        form = self.form_class(customer=request.user.customer)
        context = {"asset": obj,  "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, id_obj):
        obj = get_object_or_404(Asset, id=id_obj, customer=request.user.customer)
        c = obj.model
        if c is not None:
            c = c.category
        form = self.form_class(request.POST, instance=obj, customer=request.user.customer)
        if form.is_valid():
            new_obj = form.save()
            if c != new_obj.model.category:
                cats = dict(CATEGORY_TYPES)
                new_obj.asset_tag = "{0}{1:04d}{2:05d}".format({cats[k]: k for k in cats}[new_obj.model.get_category_display()],
                                                           request.user.customer.id, new_obj.id)
                new_obj.save()
            message = 'Asset "{0}" successfully updated.'.format(obj.asset_tag)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('assets')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request, obj.id)


class AssetNewView(View):
    template_name = 'dashboard/layouts/asset_new.html'
    form_class = AssetForm

    @method_decorator(login_required)
    def get(self, request):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to create asset. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('assets')
        form = self.form_class(customer=request.user.customer)
        context = {"form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to create asset. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('assets')
        form = self.form_class(request.POST, customer=request.user.customer)
        if form.is_valid():
            obj = form.save()
            cats = dict(CATEGORY_TYPES)
            obj.asset_tag = "{0}{1:04d}{2:05d}".format({cats[k]: k for k in cats}[obj.model.get_category_display()],
                                                       request.user.customer.id, obj.id)
            obj.save()
            request.user.customer.assets.add(obj)
            message = 'Asset "{0}" successfully added.'.format(obj.asset_tag)
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('assets')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class BilingView(View):
    template_name = 'dashboard/biling.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class InvoicesView(View):
    template_name = 'dashboard/invoices.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class InvoiceDetailView(View):
    template_name = 'dashboard/layouts/invoice_base.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class ReportsView(View):
    template_name = 'dashboard/reports.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class SoftwareView(View):
    template_name = 'dashboard/software.html'

    @method_decorator(login_required)
    def get(self, request):
        software = request.user.customer.softwares.all()
        context = {"data": software}
        return render(request, self.template_name, context)


class SoftwareShowView(View):
    template_name = 'dashboard/layouts/software_show.html'

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Software, id=id_obj, customer=request.user.customer)
        logs = obj.history.all().order_by('-timestamp')
        seats = []
        s_number = 0
        if obj.seats:
            s_number = obj.seats
        for j in obj.software.all():
            d = {}
            d['asset'] = j
            d['user'] = j.assigned_to
            d['button'] = 'Unassign'
            seats.append(d)
        for i in range(s_number - len(seats)):
            n_d = {}
            n_d['button'] = 'Assign To'
            seats.append(n_d)
        context = {'software': obj, 'history': logs, 'seats': seats}
        return render(request, self.template_name, context)


class SoftwareDuplicateView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to duplicate software. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('software')
        obj = get_object_or_404(Software, id=id_obj, customer=request.user.customer)
        clone = obj.clone()
        # f_l = clone.fullname.split('-')
        # try:
        #     clone.fullname = f_l[0] + '-' + str(int(f_l[1])+1)
        # except IndexError:
        #     clone.fullname = clone.fullname + '-' + str(1)
        # clone.save()
        request.user.customer.softwares.add(clone)
        message = 'Software "{0}" successfully duplicated.'.format(clone.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('software')


class SoftwareDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Software, id=id_obj, customer=request.user.customer)
        obj.os.clear()
        obj.software.clear()
        obj.delete()
        message = 'Software "{0}" successfully deleted.'.format(obj.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('software')


class SoftwareEditView(View):
    template_name = 'dashboard/layouts/software_edit.html'
    form_class = SoftwareForm

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Software, id=id_obj, customer=request.user.customer)
        form = self.form_class(customer=request.user.customer)
        context = {"software": obj,  "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, id_obj):
        obj = get_object_or_404(Software, id=id_obj, customer=request.user.customer)
        form = self.form_class(request.POST, instance=obj, customer=request.user.customer)
        if form.is_valid():
            form.save()
            message = 'Software "{0}" successfully updated.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('software')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request, obj.id)

class SoftwareNewView(View):
    template_name = 'dashboard/layouts/software_new.html'
    form_class = SoftwareForm

    @method_decorator(login_required)
    def get(self, request):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to create software. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('software')
        form = self.form_class(customer=request.user.customer)
        context = {"form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to create software. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('software')
        form = self.form_class(request.POST, customer=request.user.customer)
        if form.is_valid():
            obj = form.save()
            request.user.customer.softwares.add(obj)
            message = 'Software "{0}" successfully added.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('software')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class UsersView(View):
    template_name = 'dashboard/users.html'

    @method_decorator(login_required)
    def get(self, request):
        users = request.user.customer.dashusers.all()
        context = {"data": users}
        return render(request, self.template_name, context)


class UserShowView(View):
    template_name = 'dashboard/layouts/user_show.html'

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(DashUser, id=id_obj, customer=request.user.customer)
        logs = obj.history.all().order_by('-timestamp')
        assigned_assets = obj.asset_set.all()
        assigned_softwares = obj.software_set.all()
        context = {"user": obj, 'assigned_assets': assigned_assets, 'assigned_softwares': assigned_softwares, 'history':logs}
        return render(request, self.template_name, context)


class UserDuplicateView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(DashUser, id=id_obj, customer=request.user.customer)
        clone = obj.clone()
        # f_l = clone.fullname.split('-')
        # try:
        #     clone.fullname = f_l[0] + '-' + str(int(f_l[1])+1)
        # except IndexError:
        #     clone.fullname = clone.fullname + '-' + str(1)
        # clone.save()
        request.user.customer.dashusers.add(clone)
        message = 'User "{0}" successfully duplicated.'.format(clone.fullname)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('users')


class UserDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(DashUser, id=id_obj, customer=request.user.customer)
        obj.software_set.clear()
        obj.asset_set.clear()
        obj.delete()
        message = 'User "{0}" successfully deleted.'.format(obj.fullname)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('users')


class UserEditView(View):
    template_name = 'dashboard/layouts/user_edit.html'
    form_class = DashUserForm

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(DashUser, id=id_obj, customer=request.user.customer)
        form = self.form_class()
        context = {"user": obj,  "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, id_obj):
        obj = get_object_or_404(DashUser, id=id_obj, customer=request.user.customer)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            message = 'User "{0}" successfully updated.'.format(form.cleaned_data['fullname'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('users')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request, obj.id)


class UsersNewView(View):
    template_name = 'dashboard/layouts/user_new.html'
    form_class = DashUserForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            request.user.customer.dashusers.add(obj)
            message = 'User "{0}" successfully added.'.format(form.cleaned_data['fullname'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('users')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class HardwareView(View):
    template_name = 'dashboard/hardware.html'

    @method_decorator(login_required)
    def get(self, request):
        hardware = request.user.customer.hardwares.all()
        context = {"data": hardware}
        return render(request, self.template_name, context)

class HardwareDuplicateView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to duplicate hardware. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('hardware')
        obj = get_object_or_404(Hardware, id=id_obj, customer=request.user.customer)
        clone = obj.clone()
        # f_l = clone.fullname.split('-')
        # try:
        #     clone.fullname = f_l[0] + '-' + str(int(f_l[1])+1)
        # except IndexError:
        #     clone.fullname = clone.fullname + '-' + str(1)
        # clone.save()
        request.user.customer.hardwares.add(clone)
        message = 'Hardware "{0}" successfully duplicated.'.format(clone.model)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('hardware')


class HardwareDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Hardware, id=id_obj, customer=request.user.customer)
        obj.asset_set.clear()
        obj.delete()
        message = 'Hardware "{0}" successfully deleted.'.format(obj.model)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('hardware')


class HardwareEditView(View):
    template_name = 'dashboard/layouts/hardware_edit.html'
    form_class = HardwareForm

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Hardware, id=id_obj, customer=request.user.customer)
        form = self.form_class(customer=request.user.customer)
        context = {"hardware": obj,  "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, id_obj):
        obj = get_object_or_404(Hardware, id=id_obj, customer=request.user.customer)
        form = self.form_class(request.POST, instance=obj, customer=request.user.customer)
        if form.is_valid():
            form.save()
            message = 'Hardware "{0}" successfully updated.'.format(form.cleaned_data['model'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('hardware')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request, obj.id)


class HardwareNewView(View):
    template_name = 'dashboard/layouts/hardware_new.html'
    form_class = HardwareForm

    @method_decorator(login_required)
    def get(self, request):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to create hardware. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('hardware')
        form = self.form_class(customer=request.user.customer)
        context = {"form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        if int(request.user.customer.assets_count()) >= int(request.user.customer.asset_limit):
            message = 'Unable to create hardware. Asset Limit Reached!'
            messages.add_message(request, messages.ERROR, message)
            return redirect('hardware')
        form = self.form_class(request.POST, customer=request.user.customer)
        if form.is_valid():
            obj = form.save()
            request.user.customer.hardwares.add(obj)
            message = 'Hardware "{0}" successfully added.'.format(form.cleaned_data['model'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('hardware')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class CompanyView(View):
    template_name = 'dashboard/company.html'

    @method_decorator(login_required)
    def get(self, request):
        companies = request.user.customer.companies.all()
        context = {"data": companies}
        return render(request, self.template_name, context)

class CompanyDuplicateView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Company, id=id_obj, customer=request.user.customer)
        clone = obj.clone()
        # f_l = clone.fullname.split('-')
        # try:
        #     clone.fullname = f_l[0] + '-' + str(int(f_l[1])+1)
        # except IndexError:
        #     clone.fullname = clone.fullname + '-' + str(1)
        # clone.save()
        request.user.customer.companies.add(clone)
        message = 'Company "{0}" successfully duplicated.'.format(clone.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('company')


class CompanyDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Company, id=id_obj, customer=request.user.customer)
        obj.asset_set.clear()
        obj.delete()
        message = 'Company "{0}" successfully deleted.'.format(obj.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('company')


class CompanyEditView(View):
    template_name = 'dashboard/layouts/company_edit.html'
    form_class = CompanyForm

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Company, id=id_obj, customer=request.user.customer)
        form = self.form_class()
        context = {"company": obj,  "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, id_obj):
        obj = get_object_or_404(Company, id=id_obj, customer=request.user.customer)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            message = 'Company "{0}" successfully updated.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('company')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request, obj.id)


class CompanyNewView(View):
    template_name = 'dashboard/layouts/company_new.html'
    form_class = CompanyForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            request.user.customer.companies.add(obj)
            message = 'Company "{0}" successfully added.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('company')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class LocationView(View):
    template_name = 'dashboard/location.html'

    @method_decorator(login_required)
    def get(self, request):
        locations = request.user.customer.locations.all()
        context = {"data": locations}
        return render(request, self.template_name, context)


class LocationDuplicateView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Location, id=id_obj, customer=request.user.customer)
        clone = obj.clone()
        # f_l = clone.fullname.split('-')
        # try:
        #     clone.fullname = f_l[0] + '-' + str(int(f_l[1])+1)
        # except IndexError:
        #     clone.fullname = clone.fullname + '-' + str(1)
        # clone.save()
        request.user.customer.locations.add(clone)
        message = 'Location "{0}" successfully duplicated.'.format(clone.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('location')


class LocationDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Location, id=id_obj, customer=request.user.customer)
        obj.asset_set.clear()
        obj.children.clear()
        obj.delete()
        message = 'Location "{0}" successfully deleted.'.format(obj.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('location')


class LocationEditView(View):
    template_name = 'dashboard/layouts/location_edit.html'
    form_class = LocationForm

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Location, id=id_obj, customer=request.user.customer)
        form = self.form_class(customer=request.user.customer)
        context = {"location": obj,  "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, id_obj):
        obj = get_object_or_404(Location, id=id_obj, customer=request.user.customer)
        form = self.form_class(request.POST, instance=obj, customer=request.user.customer)
        if form.is_valid():
            form.save()
            message = 'Location "{0}" successfully updated.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('location')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request, obj.id)


class LocationNewView(View):
    template_name = 'dashboard/layouts/location_new.html'
    form_class = LocationForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(customer=request.user.customer)
        context = {"form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST, customer=request.user.customer)
        if form.is_valid():
            obj = form.save()
            request.user.customer.locations.add(obj)
            message = 'Location "{0}" successfully added.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('location')
        else:
            message = '{0}'.format(form.errors)
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class ManufacturersView(View):
    template_name = 'dashboard/manufacturers.html'

    @method_decorator(login_required)
    def get(self, request):
        manufacturers = request.user.customer.manufacturers.all()
        context = {"data": manufacturers}
        return render(request, self.template_name, context)


class ManufacturersDuplicateView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Manufacturer, id=id_obj, customer=request.user.customer)
        clone = obj.clone()
        # f_l = clone.fullname.split('-')
        # try:
        #     clone.fullname = f_l[0] + '-' + str(int(f_l[1])+1)
        # except IndexError:
        #     clone.fullname = clone.fullname + '-' + str(1)
        # clone.save()
        request.user.customer.manufacturers.add(clone)
        message = 'Manufacturer "{0}" successfully duplicated.'.format(clone.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('manufacturers')


class ManufacturersDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Manufacturer, id=id_obj, customer=request.user.customer)
        obj.hardware_set.clear()
        obj.delete()
        message = 'Manufacturer "{0}" successfully deleted.'.format(obj.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('manufacturers')


class ManufacturersEditView(View):
    template_name = 'dashboard/layouts/manufacturers_edit.html'
    form_class = ManufacturerForm

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Manufacturer, id=id_obj, customer=request.user.customer)
        form = self.form_class()
        context = {"manufacturer": obj,  "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, id_obj):
        obj = get_object_or_404(Manufacturer, id=id_obj, customer=request.user.customer)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            message = 'Manufacturer "{0}" successfully updated.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('manufacturers')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request, obj.id)


class ManufacturersNewView(View):
    template_name = 'dashboard/layouts/manufacturers_new.html'
    form_class = ManufacturerForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            request.user.customer.manufacturers.add(obj)
            message = 'Manufacturer "{0}" successfully added.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('manufacturers')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class SupplierView(View):
    template_name = 'dashboard/supplier.html'

    @method_decorator(login_required)
    def get(self, request):
        suppliers = request.user.customer.suppliers.all()
        context = {"data": suppliers}
        return render(request, self.template_name, context)


class SupplierDuplicateView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Supplier, id=id_obj, customer=request.user.customer)
        clone = obj.clone()
        # f_l = clone.fullname.split('-')
        # try:
        #     clone.fullname = f_l[0] + '-' + str(int(f_l[1])+1)
        # except IndexError:
        #     clone.fullname = clone.fullname + '-' + str(1)
        # clone.save()
        request.user.customer.suppliers.add(clone)
        message = 'Supplier "{0}" successfully duplicated.'.format(clone.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('supplier')


class SupplierDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Supplier, id=id_obj, customer=request.user.customer)
        obj.delete()
        message = 'Supplier "{0}" successfully deleted.'.format(obj.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('supplier')


class SupplierEditView(View):
    template_name = 'dashboard/layouts/supplier_edit.html'
    form_class = SupplierForm

    @method_decorator(login_required)
    def get(self, request, id_obj):
        obj = get_object_or_404(Supplier, id=id_obj, customer=request.user.customer)
        form = self.form_class()
        context = {"supplier": obj,  "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, id_obj):
        obj = get_object_or_404(Supplier, id=id_obj, customer=request.user.customer)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            message = 'Supplier "{0}" successfully updated.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('supplier')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request, obj.id)


class SupplierNewView(View):
    template_name = 'dashboard/layouts/supplier_new.html'
    form_class = SupplierForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            request.user.customer.suppliers.add(obj)
            message = 'Supplier "{0}" successfully added.'.format(form.cleaned_data['name'])
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('supplier')
        else:
            message = 'Something happened please try again.'
            messages.add_message(request, messages.ERROR, message)
            return self.get(request)


class AssignAssetToUser(View):
    def post(self, asset_id, user_id):
        pass


class AssignSoftwareToAsset(View):
    def post(self, software_id, asset_id):
        pass


class AssignSoftwareToUser(View):
    def post(self, software_id, user_id):
        pass
