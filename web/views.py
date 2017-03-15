from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.datetime_safe import datetime
from django.views.generic import View
from web.forms import SignUpForm, SignInForm
import datetime
from web.models import Header, Account, Setting, Feature, Demo, Client, About, Contact


class IndexView(View):
    template_name = 'web/index.html'

    def get(self, request):
        header = Header.objects.filter().first()
        setting = Setting.objects.filter().first()
        prices = Account.objects.all()
        features = Feature.objects.all()
        demos = Demo.objects.all()
        clients = Client.objects.all()
        about = About.objects.filter().first()
        contact = Contact.objects.filter().first()
        return render(request, self.template_name, locals())


class SignInView(View):
    template_name = 'signin.html'

    def get(self, request, *args, **kwargs):
        redirect_to = request.GET.get('next')
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            ffield = form.data['username_or_email']
            if '@' in ffield:
                try:
                    ffield = get_user_model().objects.get(email=ffield).username
                except ObjectDoesNotExist:
                    ffield = form.data['username_or_email']
            user = authenticate(username=ffield, password=form.data['passwrd'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.GET.get('next') is None:
                        return HttpResponseRedirect('/')
                    else:
                        return HttpResponseRedirect(request.GET.get('next'))
                else:
                    error_msg = 'Your account was locked.'
                    return render(request, self.template_name, {'form': form, 'error_msg': error_msg})
            else:
                error_msg = 'Unable to log in with provided credentials.'
                return render(request, self.template_name, {'form': form, 'error_msg': error_msg})
        else:
            error_msg = 'Some fields are empty!'
            return render(request, self.template_name, {'form': form, 'error_msg': error_msg})


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, self.template_name)
        else:
            return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['date_joined'] = datetime.date.today()
        data['last_login'] = datetime.datetime.now()
        form = SignUpForm(data)
        if form.is_valid():
            form.save()
            user = get_user_model().objects.get(username=form.data['username'], email=form.data['email'])
            user.set_password(data['password'])
            user.email = form.data['email']
            # TODO: Simdilik active!
            user.is_active = True
            user.save()
            message = 'You signed-up successfully!'
            messages.add_message(request, messages.SUCCESS, message)
            u = authenticate(username=form.data['username'], password=form.data['password'])
            login(request, u)
            return redirect('account-settings')
        else:
            error_msg = ""
            if form['username'].errors:
                error_msg += form['username'].errors
            if form['email'].errors:
                error_msg += form['email'].errors
            if form['password'].errors:
                error_msg += form['password'].errors
            return render(request, self.template_name, {'form': form, 'error_msg': error_msg})


class LogoutView(View):

    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect('/')

# HTTP Error 404
def notFoundView(request):
    template_name = '404.html'
    return render(request, template_name)

# HTTP Error 500
def serverErrorView(request):
    template_name = '500.html'
    return render(request, template_name)