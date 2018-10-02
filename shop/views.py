from typing import Dict, Any
from urllib import request

from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Product
from cart.forms import CartAddProductForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserLogInForm
from django.views import generic
from django.views.generic import View


def product_list(request):
    products = Product.objects.filter(available=True)

    context = {'products': products,
               'user': request.user}
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product,
               'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'shop/signup.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    #print(request.user.is_authenticated())
                    return redirect('/shop/')

        return render(request, self.template_name, {'form': form})


def user_login(request):
    context = {
        'form': UserLogInForm
    }
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/shop/')
        else:
            context['error'] = "Provide valid credentials"
            return render(request, 'shop/login.html', context)
    else:
        return render(request, 'shop/login.html', context)


def user_logout(request):
    if request.method == 'POST':
        logout(request)

        return render(request, "shop/login.html")






