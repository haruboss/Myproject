from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.db.models import Q


class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        card_id = request.session.get('cart_id')
        if card_id:
            cart_obj = Cart.objects.get(id=card_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


# class HomeView(EcomMixin, ListView):
#     model = Product  # queryset = Order.objects.all().order_by("-id")
#     template_name = "home.html"
#     context_object_name = 'product_list'


class HomeView(EcomMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_list = Product.objects.all().order_by("-id")
        paginator = Paginator(product_list, 6)  # Show 5 contacts per page.
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)

        context['page_obj'] = product_list
        return context


class AllProductsView(EcomMixin, TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class ProductDetailView(EcomMixin, TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()

        context['productdetail'] = product

        return context


class AddToCartView(EcomMixin, TemplateView):
    template_name = 'addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exixst
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # check item alrady exixst in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

                # new product added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price
                )
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price
            )
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context


class MyCartView(EcomMixin, TemplateView):
    template_name = 'mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart

        return context


class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()

        else:
            pass
        return redirect('EShop:mycart')


class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("EShop:mycart")


class CheckOutView(EcomMixin, CreateView):
    template_name = 'checkout.html'
    form_class = Checkoutform
    success_url = reverse_lazy('EShop:home')

    # this methods check weather customer is logged in or n
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            card_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = 'Order_Received'
            del self.request.session['cart_id']
        else:
            return redirect("EShop:home")
        return super().form_valid(form)


class CustomerRegistrationView(CreateView):
    template_name = 'customerregistration.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('EShop:home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(
            username=username, password=password, email=email)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url


class CustomerLoginView(FormView):
    template_name = 'customerlogin.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('EShop:home')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)

        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("EShop:home")


class AboutView(EcomMixin, TemplateView):
    template_name = "About.html"


class ContactView(EcomMixin, TemplateView):
    template_name = 'contact.html'


class CustomerProfileView(TemplateView):
    template_name = 'customerprofile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer

        orders = Order.objects.filter(cart__customer=customer).order_by('-id')
        context['orders'] = orders

        return context


class CustomerOrderDetailView(DetailView):
    template_name = 'customerorderdetail.html'
    model = Order
    context_object_name = 'obj_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs['pk']
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect('EShop:customerprofile')
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_keyword = self.request.GET.get('keyword')
        # search_keyword = self.request.GET['keyword']
        results = Product.objects.filter(Q(title__icontains=search_keyword) | Q(
            description__icontains=search_keyword) | Q(selling_price__icontains=search_keyword))  # imp
        context['results'] = results
        return context


class AdminLoginView(FormView):
    template_name = 'adminpages/adminlogin.html'
    form_class = AdminLoginForm
    success_url = reverse_lazy('EShop:adminhome')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)

        if usr is not None and Admin.objects.filter(user=usr).exists():

            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "invalid credentials"})

        return super().form_valid(form)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'adminpages/adminhome.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pendingorders'] = Order.objects.filter(
            order_status='Order_Received').order_by('-id')

        return context


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = 'adminpages/adminorderdetail.html'
    model = Order
    context_object_name = 'obj_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allstatus'] = view_status
        return context


class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = 'adminpages/adminorderlist.html'
    queryset = Order.objects.all().order_by("-id")
    context_object_name = 'allorders'


class AdminorderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id=order_id)
        newstatus = request.POST.get('status')
        order_obj.order_status = newstatus
        order_obj.save()

        return redirect(reverse_lazy('EShop:adminorderdetail', kwargs={"pk": self.kwargs['pk']}))

class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = 'adminpages/adminproductlist.html'
    queryset = Product.objects.all().order_by('-id')
    context_object_name = 'allproducts'


class AdminProductDetailView(AdminRequiredMixin, DetailView):
    template_name = 'adminpages/adminproductdetails.html'
    model = Product
    context_object_name = 'productdetail'


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = 'adminpages/adminproductcreate.html'
    form_class = ProductForm
    success_url = reverse_lazy('EShop:adminproductlist')

    def form_valid(self, form):
        prdt = form.save()
        images = self.request.FILES.getlist('more_images')
        for i in images:
            PI = ProductImage.objects.create(product=prdt, image=i)
            PI.save()
        return super().form_valid(form)