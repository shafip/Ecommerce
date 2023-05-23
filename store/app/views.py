from django.shortcuts import render,redirect,redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView,View,UpdateView,DeleteView,CreateView,DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse, HttpResponseBadRequest,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.utils import timezone
from PIL import Image
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from .forms import *
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from django.db.models import Prefetch
from django.contrib.sessions.backends.db import SessionStore
from django.core import serializers
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail



# Create your views here.
@login_required()
def home(request):
    return render(request,'userlogin/login.html')

def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('login_user')

@login_required(login_url='login')
def admin(request):
    return render(request,'main.html')

def user(request):
    return redirect('login_user')


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductView(ListView):
    model = Product
    template_name = 'product/productview.html'
    context_object_name = 'product'
    ordering = ['-id']



from django.contrib import messages


def productadd(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product-view')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
        # Add an error message if the form is empty
        if not request.POST:
            messages.error(request, 'Please fill out the form.')
    else:
        form = ProductForm()

    dict = {
        'form': form,
        'messages': messages.get_messages(request),
    }
    return render(request, 'product/productadd.html', dict)



@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/productupdate.html'

class ProductUpdates(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/productview.html'

def enableview(request, pk):
    ena_disa = get_object_or_404(Product, id=pk)
    if ena_disa.is_active == True:
        ena_disa.save()
    else:
        ena_disa.is_active = True
        ena_disa.save()
    return redirect('product-view')


def disableview(request, pk):
    disa = get_object_or_404(Product, id=pk)
    if disa.is_active == False:
        disa.save()
    else:
        disa.is_active = False
        disa.save()
    return redirect('product-view')
# @csrf_exempt
# def disableview(request):
#     data = QueryDict(request.body)
#     category_id = data.get('userid')
#     enable = Product.objects.get(id=category_id)
#     if enable.is_active:
#         enable.is_active = True
#
#     else:
#         enable.is_active = True
#         enable.save()
#     return redirect('product-view')



@csrf_exempt
def subproductview(request):
    variants = Varient.objects.select_related('product').order_by('-id')
    dict_form = {
        'product': variants
    }
    return render(request,'sub/subproductview.html', dict_form)


class CreateVariantView(CreateView):
    model = Varient
    template_name = 'sub/subproductadd.html'
    fields = ['product', 'image', 'image2', 'image3', 'banner', 'quantity', 'brand', 'price', 'stock']

    def form_valid(self, form):
        form.instance.product_id = self.request.POST.get('product')
        form.instance.image = self.request.FILES.get('image')
        form.instance.image2 = self.request.FILES.get('image2')
        form.instance.image3 = self.request.FILES.get('image3')
        form.instance.banner = self.request.FILES.get('banner')
        form.instance.quantity = self.request.POST.get('quantity')
        form.instance.brand = self.request.POST.get('brand')
        # form.instance.description = self.request.POST.get('description')
        form.instance.price = self.request.POST.get('price')
        form.instance.stock = self.request.POST.get('stock')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('subproductview')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


# def subproductadd(request):
#     if request.method == 'POST':
#         form = SubProductForm(request.POST)
#         if form.is_valid():
#             # product.image = request.FILES['image']
#             # product.image3 = request.FILES['image2']
#             # product.image2 = request.FILES['image3']
#             form.save()
#             return redirect('subproductview')
#         else:
#             pass
#     else:
#         form = SubProductForm()
#         dict = {
#             'forms': form
#         }
#         return render(request, 'sub/subproductadd.html', dict)
# def subproductadd(request):
#     if request.method == 'POST':
#         form = SubProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             print(form)
#             return redirect('subproductview')
#     else:
#         form = SubProductForm()
#
#     return render(request, 'sub/subproductadd.html', {'form': form})

@method_decorator(login_required(login_url='login'), name='dispatch')
class SubProductUpdate(UpdateView):
    model = Varient
    fields = ['product', 'image', 'image2', 'image3', 'banner', 'quantity', 'brand', 'price', 'stock']
    template_name = 'sub/subprojectupdate.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Varient, id=pk)
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance = self.object  # Set the instance for the form
        return form

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

    def get_context_datas(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_object'] = self.object
        return context



def enablevariant(request, pk):
    ena_disa = get_object_or_404(Varient, id=pk)
    if ena_disa.is_active == True:
        ena_disa.save()
    else:
        ena_disa.is_active = True
        ena_disa.save()
    return redirect('subproductview')


@csrf_exempt
def disablevariant(request):
    print("hey")
    data = QueryDict(request.body)
    varient_id = data.get('userid')
    disable = Varient.objects.get(id=varient_id)
    if disable.is_active:
        disable.is_active = False
        disable.save()

    else:
        disable.is_active = False
        disable.save()
    return redirect('subproductview')


@csrf_exempt
def updatedisable(request, pk):
    product = get_object_or_404(Varient, id=pk)
    if product.is_active:
        product.is_active = False
        product.save()
        response_data = {'status': 'success', 'message': 'Product disabled.'}
    else:
        response_data = {'status': 'error', 'message': 'Product is already disabled.'}
    return JsonResponse(response_data)





@method_decorator(login_required(login_url='login'), name='dispatch')
class CartView(ListView):
    model = CartItem
    template_name = 'dashbord/cart.html'
    context_object_name = 'product'
    ordering = ['-id']

    def get_queryset(self):
        queryset = CartItem.objects.select_related('varient','cart').order_by('-id')
        # cart_items = CartItem.objects.filter(cart__user=self.request.user).select_related('varient__product')
        # prefetch = Prefetch('cartitem_set', queryset=cart_items, to_attr='user_cart_items')
        # queryset = queryset.prefetch_related(prefetch)
        return queryset






# class UserProduct(ListView):
#     template_name = 'user/productview.html'
#     context_object_name = 'product'
#     ordering = ['-id']
#
#     def get_queryset(self):
#         queryset = Varient.objects.select_related('product').order_by('-id')
#         return queryset
class UserProduct(ListView):
    template_name = 'user/productview.html'
    context_object_name = 'product'
    ordering = ['-id']

    def get_queryset(self):
        queryset = Varient.objects.select_related('product').order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_detail = self.request.session.get('product_detail', {})
        context['product_detail'] = product_detail
        print("user product")

        return context



@login_required(login_url='login')
def productdetail(request, pk):
    print(pk)

    product = get_object_or_404(Varient, id=pk)
    context = {'product': product}
    return render(request, 'detailpage.html', context)

class ProductDetailView(DetailView):
    print("ProductDetailViews")
    model = Varient
    template_name = 'detailpage.html'
    context_object_name = 'product'

    def post(self, request, pk):
        # request.session.flush()
        print("post")

        # Get product from the database or show 404 error
        varient = get_object_or_404(Varient, id=pk)
        print(pk)

        # request.session.flush()

        # Get session key or generate a new one
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key

        # Get cart from session or create a new one
        product_detail = request.session.get('product_detail', {})

        product_detail[pk] = {
            'price': varient.price,
            'brand': varient.brand,
            'quantity':varient.quantity,
            'name': varient.product.name,
            'image_url': varient.image.url,
            'product_id': varient.id
        }
        request.session['product_detail'] = product_detail
        request.session.modified = True
        print(product_detail)
        return redirect('product-detail',pk=pk)


def add_to_carts(request, product_id):
    varient = get_object_or_404(Varient, id=product_id)
    cart, created = Users.objects.get_or_create(email=request.user.email)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, varient=varient, )
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{varient.product.name} has been added to your cart!")
    return redirect('cart')





@csrf_exempt
def add_to_cart(request, product_id):
    if request.method == 'POST':
        varient = get_object_or_404(Varient, id=product_id)
        user, created = Users.objects.get_or_create(email=request.user.email)
        cart_item, created = CartItem.objects.get_or_create(cart=user, varient=varient)
        product = varient.stock

        if product <= cart_item.quantity:
            data = {'success': False}
        else:
            cart_item.quantity += 1
            cart_item.save()
            data = {'success': True}

        return JsonResponse(data)
    else:
        data = {'success': False}
        return JsonResponse(data)







def cart_updates(request, pk, action):
    cart_item = get_object_or_404(CartItem, id=pk)
    product = cart_item.varient
    if action == 'increment':
        if product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, f"Sorry, {product.product.name} only {product.stock}  available in stock.")
    elif action == 'decrement':
        cart_item.quantity -= 1  # Decrement quantity by 1
        cart_item.save()

    return redirect('cart')






from django.template.loader import render_to_string
@csrf_exempt
def product_cart_updates(request, pk, action):
    product = get_object_or_404(CartItem, id=pk)
    varient = product.varient

    if action == 'increment':
        if varient.stock > product.quantity:
            varient.quantity += 1
            varient.save()
        else:
            messages.warning(request, f"Sorry, {varient.product.name} only {varient.stock}  available in stock.")
    if action == 'increment':
        product.quantity += 1
    elif action == 'decrement':
        product.quantity -= 1
    product.save()


    cart_item_template = 'cart/change_cart.html'
    context = {'item': CartItem.objects.filter(id=pk)}
    cart_item_html = render_to_string(cart_item_template, context)


    data = {'html': cart_item_html, 'pk': pk}
    return JsonResponse(data)

@csrf_exempt
def add_to_wishlist(request, product_id):
    variant = get_object_or_404(Varient, id=product_id)

    if Wishlist.objects.filter(varient=variant, cart=request.user).exists():
        data = {
            'success': False,
        }
        return JsonResponse(data)
    else:
        if request.method == 'POST':
            user, created = Users.objects.get_or_create(email=request.user.email)
            wishlist_item, created = Wishlist.objects.get_or_create(cart=user, varient=variant)
            wishlist_item.save()
            data = {
                'success': True,
            }
            return JsonResponse(data)
        else:
            return HttpResponseBadRequest('Invalid Request')





def wishlist(request):

        cart = Users.objects.get(email=request.user.email)
        wishlist_items = Wishlist.objects.filter(cart=cart).select_related('cart','varient__product')
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
        # try:
        #     return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
        # except:
        #     pass




def wishtocart(request, product_id):
    cart = Users.objects.get(email=request.user.email)
    varient = get_object_or_404(Varient, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, varient=varient)
    cart_item.quantity += 1
    cart_item.save()
    Wishlist.objects.filter(cart=cart, varient=varient).delete()
    return redirect('cart')
from django.urls import reverse_lazy

#
class YourModelDeleteView(DeleteView):
    model = Wishlist
    template_name = 'wishlist.html'
    success_url = reverse_lazy('wishlist')



# def checkout(request):
#     cart = Users.objects.get(user=request.user)
#     order_items = []
#     total_quantity = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))['quantity__sum'] or 0
#     cart_items = CartItem.objects.filter(cart=cart).order_by('-id')
#     total = cart_items.annotate(
#         total_price=ExpressionWrapper(
#             F('varient__price') * F('quantity'),
#             output_field=FloatField()
#         )
#     ).aggregate(
#         total=Sum('total_price')
#     )['total'] or 0
#
#     user_shippings = Shipping.objects.filter(user=cart).order_by('-id')
#     if request.method == 'POST':
#         shipping_form = ShippingForm(request.POST)
#         if shipping_form.is_valid():
#             selected_item_id = shipping_form.cleaned_data['selected_item']
#             shipping_id = shipping_form.cleaned_data['shipping_id']
#             shipping_object = Shipping.objects.get(user=cart, id=shipping_id)
#             for cart_item in cart_items:
#                 order_item = Order.objects.create(
#                     quantity=cart_item.quantity,
#                     varient=cart_item.varient,
#                     user=cart_item.cart,
#                     price=cart_item.price,
#                     shipping=shipping_object,
#                 )
#                 order_items.append(order_item)
#                 cart_item.delete()
#             messages.success(request, 'Item added to cart successfully!')
#             return redirect('ordersuccess')
#     else:
#         shipping_form = ShippingForm()
#
#     context = {
#         'order_items': order_items,
#         'form': shipping_form,
#         'cart_items': cart_items,
#         'total': total,
#         'total_quantity': total_quantity,
#         'user_shippings': user_shippings,
#     }
#
#     return render(request, 'checkout/checkout.html', context)

from django.db.models import F, ExpressionWrapper, FloatField, Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import ShippingForm


# def checkout(request):
#     # Retrieve the user's cart and associated cart items
#     cart = Users.objects.get(email=request.user.email)
#     cart_items = CartItem.objects.filter(cart=cart).order_by('-id')
#     order_items=[]
#     # Calculate the total quantity and price of items in the cart
#     total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
#     total = cart_items.annotate(
#         total_price=ExpressionWrapper(
#             F('varient__price') * F('quantity'),
#             output_field=FloatField()
#         )
#     ).aggregate(
#         total=Sum('total_price')
#     )['total'] or 0
#
#     # Retrieve the user's shipping addresses
#     user_shippings = Shipping.objects.filter(user=cart).order_by('-id')
#
#     # Handle the POST request when the user submits the form
#     if request.method == 'POST':
#         # Get the selected shipping address
#         address_id = request.POST.get('address_id')
#         selected_address = Shipping.objects.get(id=address_id)
#
#         # Create an order item for each cart item and associate it with the selected address
#         order_items = []
#         for cart_item in cart_items:
#             order_item = OrderItem.objects.create(
#                 quantity=cart_item.quantity,
#                 user=cart_item.cart,
#                 price=cart_item.price,
#                 shipping=selected_address
#             )
#             order_items.append(order_item)
#             cart_item.delete()
#
#         # Create a new order for the user based on their order items
#         order = Order.objects.create(
#             user=cart,
#             date=timezone.now(),
#             items=total_quantity,
#             total=total,
#             orderitem=order_items[0]
#         )
#
#         # Redirect the user to a success page
#         return redirect('ordersuccess')
#
#     # Handle the GET request when the user first loads the page
#     else:
#         shipping_form = ShippingForm()
#
#     # Render the checkout page with the necessary context data
#     context = {
#         'order_items': order_items,
#         'form': shipping_form,
#         'cart_items': cart_items,
#         'total': total,
#         'total_quantity': total_quantity,
#         'user_shippings': user_shippings,
#     }
#     return render(request, 'checkout/checkout.html', context)

@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        # If user is logged in
        user = request.user
        order_items = []
        cart_items = CartItem.objects.filter(cart=user)
        total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        user_shippings = Shipping.objects.filter(user=user)
        total = cart_items.annotate(
                total_price=ExpressionWrapper(
                    F('varient__price') * F('quantity'),
                    output_field=FloatField()
                )
            ).aggregate(
                total=Sum('total_price')
            )['total'] or 0

        if request.method == 'POST':
            # Get the selected shipping address
            address_id = request.POST.get('address_id')
            selected_address = Shipping.objects.get(id=address_id)

            # Create an order with the selected address
            order = Orders.objects.create(
                items=total_quantity,
                user=user,
                total_amount=total,
                shipping=selected_address,
                date=timezone.now(),
            )

            # Create order items for each cart item and delete the cart items
            for cart_item in cart_items:
                order_item = OrderItems.objects.create(
                        order=order,
                        quantity=cart_item.quantity,
                        price=cart_item.price,
                        varient=cart_item.varient,
                        is_completed=True,
                    )
                order_items.append(order_item)
                cart_item.delete()
                subject = 'Order Created'
                message = 'Your Order has been successfully created.'
                recipient_email = user.email

                # Render the HTML template
                html_message = render_to_string('orderemail.html', {'message': message, 'order':order_items })

                # send_mail(
                #     subject,
                #     message,
                #     settings.DEFAULT_FROM_EMAIL,
                #     [recipient_email],
                #     html_message=html_message
                # )

            return redirect('ordersuccess', order_id=order.id)
        else:
            shipping_form = ShippingForm()

        context = {
            'order_items': order_items,
            'form': shipping_form,
            'cart_items': cart_items,
            'total': total,
            'total_quantity': total_quantity,
            'user_shippings': user_shippings,
        }

        return render(request, 'checkout/checkout.html', context)
    else:
        redirect('login')





# from django.conf import settings
# def order_confirmation(user, order):
#     subject = 'Order Confirmation'
#     template = 'orderemail.html'
#     context = {'username': user, 'order': order}
#     email_content = render_to_string(template, context)
#     send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=email_content)

@login_required(login_url='login')
def checkoutform(request):
    cart = Users.objects.get(email=request.user.email)
    order_items = []
    total_quantity = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))[
                         'quantity__sum'] or 0
    cart_items = CartItem.objects.filter(cart=cart).order_by('-id')
    total = cart_items.annotate(
        total_price=ExpressionWrapper(
            F('varient__price') * F('quantity'),
            output_field=FloatField()
        )
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            user = Users.objects.get(email=request.user.email)
            shipping.user = user
            shipping.save()
            return redirect('check_out')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = ShippingForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'total_quantity': total_quantity,

    }

    return render(request, 'checkout/shippingform.html', context)




@login_required(login_url='profile')
def profile(request):
    if request.user.is_superuser:
        return redirect('main.html')
    else:
        return redirect('base.html')



def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'login/register.html', context)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=raw_password)
            if user is not None:
                login(request, user)

            else:
                messages.error(request, 'Authentication Failed')
        else:
            messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'login/register.html', context)

    return render(request, 'login/register.html', {})





from django.contrib.auth.decorators import login_required

def useraddress(request):
    cart = Users.objects.get(email=request.user.email)
    shipping_addresses = Shipping.objects.filter(user=cart)
    context = {'user': cart, 'shipping_addresses': shipping_addresses}
    return render(request, 'useraddress.html', context)
@method_decorator(login_required(login_url='login'), name='dispatch')
class CartDelete(DeleteView):
    model = CartItem
    template_name = 'cart/cart.html'
    success_url = reverse_lazy('cart')

@method_decorator(login_required(login_url='login'), name='dispatch')
class delete_cart_product(DeleteView):
    model = CartItem
    success_url = reverse_lazy('cart')
    http_method_names = ['post']

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        product_id = self.object.product_id
        self.object.delete()
        data = {
            'success': True,
            'message': 'Product deleted successfully.',
            'product_id': product_id
        }
        return JsonResponse(data)



@login_required(login_url='login')
def myorder(request):
    print("myorder")
    cart = Users.objects.get(email=request.user.email)
    my_order = Orders.objects.filter(user=cart).order_by('-id')
    order_item = OrderItems.objects.filter(order__in=my_order.values_list('id', flat=True))
    context = {'user': cart, 'myorder': my_order,'order_item':order_item}
    return render(request, 'myorder.html', context)

@login_required(login_url='login')
def myorder_detail(request, order_id):
    # Fetch the order with the given order_id
    # order = get_object_or_404(Orders, id=order_id)
    order = get_object_or_404(Orders.objects.select_related('shipping','user'), id=order_id)

    # Fetch the order items related to the order, along with their variant and order objects,
    # using prefetch_related to minimize database queries
    products = OrderItems.objects.filter(order=order).select_related('varient')

    # Render the template with the order and products data
    return render(request, 'myorderdetails.html', {'order': order, 'products': products})




@login_required(login_url='login')
def UserProfileView(request):
    user_profile = Users.objects.get(email=request.user.email)
    return render(request, 'profile.html', {'user_profile': user_profile})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Users
from .forms import UsersEditForm

@login_required(login_url='login')
def edit_profile(request):
    user = get_object_or_404(Users, id=request.user.id)  # Get the logged-in user

    if request.method == 'POST':
        form = UsersEditForm(request.POST, request.FILES, instance=user)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('myprofile')
    else:
        form = UsersEditForm(instance=user)

    return render(request, 'profileupdate.html', {'form': form})


@login_required(login_url='login')
def changepswd(request):
    user = get_object_or_404(Users, id=request.user.id)  # Get the logged-in user
    if request.method == 'POST':
        form = PswdForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('myprofile')
    else:
        form = PswdForm(instance=user)
    return render(request, 'changepswd.html', {'form': form})








@method_decorator(login_required(login_url='login'), name='dispatch')
class OrderList(ListView):
    model = Orders
    template_name = 'order.html'
    context_object_name = 'order'
    ordering = ['-id']
    queryset = Orders.objects.select_related('user', 'shipping').prefetch_related(
        Prefetch('shipping', queryset=Shipping.objects.prefetch_related('name'))
    )




# def userorderdetails(request, user_id):
#     # Get the user object or return a 404 error if it doesn't exist
#     user = get_object_or_404(User, id=user_id)
#     # Get all orders for the user, and prefetch related variant objects to avoid N+1 queries
#     orders = Order.objects.filter(user=user).select_related('varient')
#     context = {'user': user, 'orders': orders}
#     return render(request, 'orderdetails.html', context)
# def order(request):
#
#     users = Users.objects.all()
#     user_orders = []
#     for user in users:
#         orders = OrderItem.objects.select_related('varient').filter(user=user)
#         if orders:
#             total_items = 0
#             total_price = 0.0
#             order_dates = []
#             for order in orders:
#                 total_items += order.quantity
#                 total_price += order.price * order.quantity
#                 order_dates.append(order.date)
#             latest_order_date = max(order_dates)
#             order_item = Order.objects.create(
#                 user=user,
#                 date=latest_order_date,
#                 items=total_items,
#                 total=total_price
#             )
#             user_orders.append(order_item)
#     context = {'user_orders': user_orders}
#     return render(request, 'ordersuccess.html', context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class OrderSuccessView(ListView):
    model = Orders
    template_name = 'ordersuccess.html'
    context_object_name = 'order'

    def get_cart_items_by_order_id(self, order_id):
        order = get_object_or_404(Orders, id=order_id)
        products = OrderItems.objects.filter(order_id=order)
        total_items = products.aggregate(Sum('quantity'))['quantity__sum']
        total_amount = products.annotate(
            total_price=ExpressionWrapper(
                F('varient__price') * F('quantity'),
                output_field=FloatField()
            )
        ).aggregate(Sum('total_price'))['total_price__sum']
        return total_items, total_amount, products.annotate(total_price=ExpressionWrapper(
            F('varient__price') * F('quantity'),
            output_field=FloatField()
        ))



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')  # Assumes order_id is passed in URL kwargs
        total_items, total_amount, products = self.get_cart_items_by_order_id(order_id)
        context['total_items'] = total_items
        context['total_amount'] = total_amount
        context['products'] = products

        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class DirectOrdersuccess(ListView):
    print("direct order success")
    model = Orders
    template_name = 'successorder.html'
    context_object_name = 'order'

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Orders, id=order_id)
        print(order_id)

        products = OrderItems.objects.filter(order_id=order)

        return products



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Orders, id=order_id)
        products = get_object_or_404(OrderItems, id=order_id)
        context['order'] = order
        context['products'] = products
        return context

@login_required
def delete_user(request, user_id):
    user = Users.objects.get(id=user_id)
    user.delete()
    return redirect('login')

@login_required(login_url='login')
def cartquantity(request):
    user = Users.objects.get(email=request.user.email)
    total_quantity = CartItem.objects.filter(cart=user).aggregate(Sum('quantity'))[
                         'quantity__sum'] or 0
    context = {
        'total_quantity': total_quantity,
    }
    return render(request, 'base.html', context)
@method_decorator(login_required(login_url='login'), name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'userlogin/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('userproduct')  # Replace with your desired success URL

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password')
        return super().form_invalid(form)
@login_required(login_url='login')
def ProfileView(request):
    print("hey user")
    model = Users.objects.all()

    context = {'userss':model}
    return render(request,'user profile.html',context)






@login_required(login_url='login')
def order_detail(request, order_id):
    # Fetch the order with the given order_id
    # order = get_object_or_404(Orders, id=order_id)
    order = get_object_or_404(Orders.objects.select_related('shipping','user'), id=order_id)

    # Fetch the order items related to the order, along with their variant and order objects,
    # using prefetch_related to minimize database queries
    products = OrderItems.objects.filter(order=order).select_related('varient')

    # Render the template with the order and products data
    return render(request, 'orderdetails.html', {'order': order, 'products': products})



@login_required(login_url='login')
def directbuy(request, product_id):
    print("directbuy")
    user = Users.objects.get(email=request.user.email)
    varient = get_object_or_404(Varient, id=product_id)
    print(product_id)
    order_items = []
    user_shippings = Shipping.objects.filter(user=user).order_by('-id')
    shipping_form = None  # Initialize shipping_form with None

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        selected_address = Shipping.objects.get(id=address_id)
        order = Orders.objects.create(
            items=1,
            user=user,
            total_amount=varient.price,
            shipping=selected_address,
            date=timezone.now(),
        )
        if varient:
            order_item = OrderItems.objects.create(
                    order=order,
                    quantity=1,
                    price=varient.price,
                    varient=varient,
                )
            order_items.append(order_item)
            print(order_item.id)

        return redirect('directordersuccess', order_id=order.id)
    else:
        shipping_form = ShippingForm()



    context = {
        'order_items': order_items,
        'form': shipping_form,
        'product_items': varient,
        'user_shippings': user_shippings,
    }
    return render(request, 'direcctorder.html', context)



@login_required(login_url='login')
def directorderform(request,product_id):
    varient = get_object_or_404(Varient,id=product_id)
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            user = Users.objects.get(email=request.user.email)
            shipping.user = user
            shipping.save()
            return redirect('check_out')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = ShippingForm()

    context = {
        'form': form,
        'product':varient,
    }

    return render(request, 'directorderform.html', context)

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            cart = request.session.get('cart', {})
            cart_items = CartItem.objects.filter(cart=user)

            for item in cart.values():
                print(item, 'item after login')
                found_item = False

                for cart_item in cart_items:
                    if cart_item.varient.product.name == item['name']:
                        cart_item.quantity += 1
                        cart_item.save()
                        found_item = True
                        print(cart_item)
                        print("Yes")
                        break

                if not found_item:
                    variants = Varient.objects.filter(product__name=item['name'])

                    if variants.exists():
                        variant = variants.first()
                        cart_item = CartItem(
                            varient=variant,
                            quantity=item['quantity'],
                            price=item['price'],
                            cart=user
                        )
                        cart_item.save()
                        print("Added cart item successfully")

            wish = request.session.get('wish', {})
            wish_items = Wishlist.objects.filter(cart=user)
            for item in wish.values():
                print(item, 'item after login')
                found_item = False

                for wish_item in wish_items:
                    if wish_item.varient.product.name == item['name']:
                        found_item = True
                        break

                if not found_item:
                    variants = Varient.objects.filter(product__name=item['name'])

                    if variants.exists():
                        variant = variants.first()
                        wish_item = Wishlist(
                            varient=variant,
                            cart=user
                        )
                        wish_item.save()
                        print("Added wish item successfully")




            #
            # next_url = request.POST.get('next')
            #
            # if next_url:
            #     return redirect(next_url)
            # return redirect('dashboard')


            next_url = request.POST.get('next')
            if next_url:
                return JsonResponse({'success': True, 'redirect': next_url})
            else:
                return JsonResponse({'success': True, 'redirect': 'accounts/dashboard/'})
        else:
            return JsonResponse({'success': False,})
            # error_msg = 'Invalid email or password'
            return render(request, 'userlogin/login.html', {'error_msg': error_msg})

    else:
        return render(request, 'userlogin/login.html')




# @method_decorator(login_required(login_url='login'), name='dispatch')
# class MyPasswordChangeView(PasswordChangeView):
#     # form_class = MyPasswordChangeForm
#     # template_name = 'passwordchange/password_change.html'
#     # success_url = reverse_lazy('myprofile')
#     template_name = 'user/change password.html'
#     # success_url = '/myprofile/'

class MyPasswordChangeView(View):
    template_name = 'userlogin/change password.html'
    form_class = MyPasswordChangeForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('myprofile')  # Replace with the desired URL or view name
            else:
                form.add_error('old_password', 'Invalid old password')

        return render(request, self.template_name, {'form': form})





from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('logoutss')



class GuestAddToCartView(View):
    def post(self, request, product_id):
        # Get product from the database or show 404 error

        product = get_object_or_404(Varient, id=product_id)
        product_stock = product.stock
        # request.session.flush()

        # Get session key or generate a new one
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key

        # Get cart from session or create a new one
        cart = request.session.get('cart', {})

        data = {'success': False}

        if product_stock <= cart.get('quantity', 0):
            data = {'success': False}
            return JsonResponse(data)
        else:
            # Add product to cart with default quantity of 1
            cart[product_id] = {
                'quantity': 1,
                'price': product.price,
                'brand': product.brand,
                'name': product.product.name,
                'image_url': product.image.url,
                'product_id': product.id
            }
        request.session['cart'] = cart
        request.session.modified = True
        print(request.session['cart'])
        data = {
            'success': True,
        }
        return JsonResponse(data)




class CartDetailView(View):
    def get(self, request):
        # Get cart from session or create a new one
        cart = request.session.get('cart', {})

        total_quantity = sum(item['quantity'] for item in cart.values())
        total_amount = sum(item['quantity'] * item['price'] for item in cart.values())
        total_price = cart.get('quantity', 0) * cart.get('price', 0)




        context = {
            # 'product': product,
            # 'quantity': quantity,
            'price': total_price,
            'total_quantity': total_quantity,
            'total_amount': total_amount,
            # 'brand': brand,
            # 'name': name,
            'cart': cart,

        }

        return render(request, 'guestcart/cart.html', context=context)





from django.template.loader import render_to_string

# def update_varient(request, pk):
#     my_instance = get_object_or_404(Varient, pk=pk)
#     form = SubProductForm(request.POST or None, instance=my_instance)
#     if form.is_valid():
#         form.save()
#         table_html = render_to_string('sub/subproductview.html', {
#             'varients': Varient.objects.all()
#         })
#         return redirect('subproductview')
#
#     context = {
#         'form': form,
#         'my_instance': my_instance,
#     }
#     return render(request, 'ajax form/varient_update.html', context)





@method_decorator(login_required(login_url='login'), name='dispatch')
class Cart_To_Wish(View):
    @csrf_exempt
    def post(self, request, product_id):
        varient = get_object_or_404(Varient, id=product_id)
        user, created = Users.objects.get_or_create(email=request.user.email)


        wish_list_exists = Wishlist.objects.filter(cart=user, varient=varient).exists()
        cart_item = CartItem.objects.filter(cart=user, varient=varient).first()
        if cart_item:
            cart_item.delete()
            return redirect('cart')


        if not wish_list_exists:
            wish_list = Wishlist.objects.create(cart=user, varient=varient)
            wish_list.save()

            # Delete the item from the user's cart
            cart_item = CartItem.objects.filter(cart=user, varient=varient).first()
            if cart_item:
                cart_item.delete()

            # Return a JSON response indicating success
            response_data = {'success': True, 'message': 'Added to Wishlist successfully!'}
            return JsonResponse(response_data)








# from django.conf import settings
# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#
#         if password1 != password2:
#             return render(request, 'signup.html', {'error': 'Passwords do not match.'})
#
#         try:
#             Users.objects.get(email=email)
#             exists = True
#             return JsonResponse({'exists': exists})
#         except Users.DoesNotExist:
#             user = Users.objects.create_user(name=name, email=email, password=password1, phone_number=phone_number)
#             user.save()
#
#             # Authenticate and login the user
#             user = authenticate(request, email=email, password=password1)
#             login(request, user)
#
#             if user.is_authenticated:
#                 # Send email notification
#                 subject = 'Account Created'
#                 message = 'Your account has been successfully created.'
#                 recipient_email = user.email
#                 send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
#
#                 # Update cart items
#                 cart = request.session.get('cart', {})
#                 cart_items = CartItem.objects.filter(cart=user)
#
#                 for item in cart.values():
#                     found_item = False
#
#                     for cart_item in cart_items:
#                         if cart_item.varient.product.name == item['name']:
#                             cart_item.quantity += 1
#                             cart_item.save()
#                             found_item = True
#                             break
#
#                     if not found_item:
#                         variants = Varient.objects.filter(product__name=item['name'])
#
#                         if variants.exists():
#                             variant = variants.first()
#                             cart_item = CartItem(
#                                 varient=variant,
#                                 quantity=item['quantity'],
#                                 price=item['price'],
#                                 cart=user
#                             )
#                             cart_item.save()
#
#                 # Update wishlist items
#                 wish = request.session.get('wish', {})
#                 wish_items = Wishlist.objects.filter(cart=user)
#
#                 for item in wish.values():
#                     found_item = False
#
#                     for wish_item in wish_items:
#                         if wish_item.varient.product.name == item['name']:
#                             found_item = True
#                             break
#
#                     if not found_item:
#                         variants = Varient.objects.filter(product__name=item['name'])
#
#                         if variants.exists():
#                             variant = variants.first()
#                             wish_item = Wishlist(
#                                 varient=variant,
#                                 cart=user
#                             )
#                             wish_item.save()
#
#                 next_url = request.POST.get('next')
#                 if next_url:
#                     return redirect(next_url)
#
#                 return redirect('dashboard')
#
#     return render(request, 'signup.html')

from django.conf import settings
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})


        try:
            Users.objects.get(email=email)
            return render(request, 'signup.html', {'error': 'Email already exists.'})
        except Users.DoesNotExist:
            pass

        user = Users.objects.create_user(name=name, email=email, password=password1,phone_number=phone_number)
        user.save()

        # Authenticate user and redirect to home page

        user = authenticate(request, email=email, password=password1)
        login(request, user)
        subject = 'Account Created'
        message = 'Your account has been successfully created.'
        recipient_email = user.email  # Assuming 'user' is the newly registered user
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
        cart = request.session.get('cart', {})
        cart_items = CartItem.objects.filter(cart=user)

        for item in cart.values():
            print(item, 'item after login')
            found_item = False

            for cart_item in cart_items:
                if cart_item.varient.product.name == item['name']:
                    cart_item.quantity += 1
                    cart_item.save()
                    found_item = True
                    print(cart_item)
                    print("Yes")
                    break

            if not found_item:
                variants = Varient.objects.filter(product__name=item['name'])

                if variants.exists():
                    variant = variants.first()
                    cart_item = CartItem(
                        varient=variant,
                        quantity=item['quantity'],
                        price=item['price'],
                        cart=user
                    )
                    cart_item.save()
                    print("Added cart item successfully")

        wish = request.session.get('wish', {})
        wish_items = Wishlist.objects.filter(cart=user)
        for item in wish.values():
            print(item, 'item after login')
            found_item = False

            for wish_item in wish_items:
                if wish_item.varient.product.name == item['name']:
                    found_item = True
                    break

            if not found_item:
                variants = Varient.objects.filter(product__name=item['name'])

                if variants.exists():
                    variant = variants.first()
                    wish_item = Wishlist(
                        varient=variant,
                        cart=user
                    )
                    wish_item.save()
                    print("Added wish item successfully")
        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)

        return redirect('dashboard')

    return render(request, 'signup.html')



@method_decorator(login_required(login_url='login'), name='dispatch')
class CartViews(View):
    template_name = 'cart/cart.html'

    def get(self, request):
        cart = Users.objects.get(email=request.user.email)
        cart_items = CartItem.objects.filter(cart=cart).order_by('-id').select_related('cart', 'varient__product')
        for item in cart_items:
            print("id:",item.varient.id)
            print("name:", item.varient.product.name)

        # Ensure that all quantities are greater than or equal to 1
        for item in cart_items:
            if item.quantity < 1:
                item.quantity = 1
                item.save()
                messages.warning(request, f"Minimum quantity for {item.varient.product.name} is 1")

        total_quantity = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))['quantity__sum'] or 0
        total = cart_items.annotate(
            total_price=ExpressionWrapper(
                F('varient__price') * F('quantity'),
                output_field=FloatField()
            )
        ).aggregate(
            total=Sum('total_price')
        )['total'] or 0

        is_empty = not cart_items.exists()

        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'is_empty': is_empty,
            'total': total
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')
        cart_item = CartItem.objects.get(pk=pk)
        product_id = cart_item.product_id
        cart_item.delete()

        # Add items to the cart using the session

        data = {
            'success': True,
            'message': 'Product deleted successfully.',
            'product_id': product_id
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = CartItem.objects.filter(cart=self.request.user)
        return context


def delete_product(request, product_id):
    cart = request.session.get('cart', {})
    for cart_product_id in cart.keys():
        print(cart_product_id)
        if str(cart_product_id) == str(product_id):
            del cart[cart_product_id]
            request.session.modified = True
            break
    return redirect('cart_detail')




def guest_cart_updates(request, pk, action):
    print(pk)
    # Get the cart from the session data
    cart = request.session.get('cart', {})

    for cart_product_id in cart.keys():
        print(cart_product_id)
        if str(cart_product_id) == str(pk):
            if action == 'increment':
                cart[cart_product_id]['quantity'] += 1
            elif action == 'decrement':
                cart[cart_product_id]['quantity'] -= 1



    request.session['cart'] = cart
    return redirect('cart_detail')


class GuestAddToWishView(View):
    def post(self, request, product_id):
        # Get product from the database or show 404 error
        product = get_object_or_404(Varient, id=product_id)
        print(product_id)

        # request.session.flush()

        # Get session key or generate a new one
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key

        # Get cart from session or create a new one
        wishlist = request.session.get('wish', {})

        if str(product_id) in wishlist:
            data = {
                'success': False,
            }
            return JsonResponse(data)


        else:
            # Add product to cart with default quantity of 1
            wishlist[product_id] = {
                'price': product.price,
                'brand': product.brand,
                'name': product.product.name,
                'image_url': product.image.url,
                'product_id': product.id
            }
        request.session['wish'] = wishlist
        request.session.modified = True
        print(request.session['wish'])
        data = {
            'success': True,
        }
        return JsonResponse(data)





class WishDetailView(View):
    def get(self, request):

        wish = request.session.get('wish', {})
        print(wish)

        context = {
            'wish': wish,
        }

        return render(request, 'guestcart/wish.html', context=context)


def delete_wish_product(request, product_id):
    print("hi")
    print(product_id)
    wishlist = request.session.get('wish', {})
    for wish_product_id in wishlist.keys():
        print(wish_product_id)
        if str(wish_product_id) == str(product_id):
            del wishlist[wish_product_id]
            request.session.modified = True
            break
    return redirect('wish_detail')




def change_order_status(request, pk):
    order = get_object_or_404(Orders, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.status = new_status
        order.save()
        return redirect('orderlist')  # Redirect to order detail page

    return render(request, 'trackorder.html', {'order': order})



@csrf_exempt
def cancel_order(request, order_id):
    print(order_id)
    if request.method == 'POST':
        select_option = request.POST.get('select_option')
        message = request.POST.get('message')
        try:
            order = OrderItems.objects.get(id=order_id)
        except OrderItems.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'})

        # Update the attributes of the fetched Orders instance
        order.reason = select_option
        order.messages = message
        order.is_completed = False
        order.save()

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})

    # Return a JSON response indicating failure if the request method is not POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def product_list(request):
    products = Varient.objects.select_related('product').filter(is_active=True)

    product = Product.objects.filter(is_active=True)
    product_detail = request.session.get('product_detail', {})



    context = {
        'filter_product':product,
        'products': products,
        # 'form': form,
        'banner':products,
        'recsentview': product_detail

    }
    return render(request, 'logeduserview.html', context)

# def product_list(request):
#     products = Varient.objects.filter(is_active=True)
#     product_detail = request.session.get('product_detail', {})
#
#
#     if request.method == 'GET' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         selected_value = request.GET.get('selected_value')  # Get the selected value from the AJAX request
#
#         # Filter the products based on the selected value
#         filtered_products = Product.objects.filter(name=selected_value).values('id', 'name')
#
#         # Convert the filtered products queryset to a list of dictionaries
#         products_list = list(filtered_products)
#
#         # Return the filtered products as JSON response
#         return JsonResponse(products_list, safe=False)
#
#     context = {
#         'products': products,
#         'banner': products,
#         'recsentview': product_detail
#     }
#     return render(request, 'logeduserview.html', context)




class GuestDirectBuy(View):
    print("GuestDirectBuy")
    def post(self, request, product_id):
        # Get product from the database or show 404 error
        varient = get_object_or_404(Varient, id=product_id)
        print(product_id)

        # request.session.flush()

        # Get session key or generate a new one
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key

        # Get cart from session or create a new one
        product = request.session.get('product', {})

        product[product_id] = {
                'price': varient.price,
                'brand': varient.brand,
                'name': varient.product.name,
                'image_url': varient.image.url,
                'product_id': varient.id
            }
        request.session['product'] = product
        request.session.modified = True
        return redirect('direct_buy',product_id=varient.id)


class RecentlyView(View):
    def post(self, request, product_id):
        # Get product from the database or show 404 error
        varient = get_object_or_404(Varient, id=product_id)
        print(product_id)

        # request.session.flush()

        # Get session key or generate a new one
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key

        # Get cart from session or create a new one
        product = request.session.get('product', {})

        product[product_id] = {
                'price': varient.price,
                'brand': varient.brand,
                'name': varient.product.name,
                'image_url': varient.image.url,
                'product_id': varient.id
            }
        request.session['product'] = product
        request.session.modified = True
        return redirect('direct_buy',product_id=varient.id)


from django.shortcuts import redirect


def re_order(request, order_id):
    order_items = OrderItems.objects.filter(order__order_id=order_id)  # Filter by slug field
    print(order_id)
    print(order_items)

    for item in order_items:
        print(item,'w')
        cart_item, created = CartItem.objects.get_or_create(
            cart=item.order.user,
            varient=item.varient,
            price=item.price,
            quantity=item.quantity
        )
        cart_item.save()
        print(cart_item)

    return redirect('cart')



def admin_order_approves(request, product_id):
    order = get_object_or_404(OrderItems, id=product_id)
    print(product_id)
    context = {
        'reason':order
    }
    return render(request,'ordercancelapprove.html',context)


def admin_order_approves_updation(request, product_id, action):
    order = get_object_or_404(OrderItems, id=product_id)
    status = order.order.status
    varient = order.varient
    stock = varient.stock
    print(stock, "h")
    print(order.quantity, "he")

    if action == 'approved':
        order.status = "return approved"
        stock += order.quantity
        varient.stock = stock

        order.save()  # Save the updated order status
        varient.save()  # Save the updated variant stock
        # Save the updated status in the field Orders
        order.order.status = "cancel"
        order.order.save()


    elif action == 'reject':
        order.status = "return rejected"
    else:
        return HttpResponse("Error occurred")

    order.save()


    return redirect('orderlist')

def filter_products(request):
    selected_value = request.GET.get('selected_value')

    # Filter the products based on the selected value
    filtered_products = Varient.objects.select_related('product').filter(product__name=selected_value)


    # Prepare the filtered products as JSON data
    products_data = []
    for product in filtered_products:
        products_data.append({
            'name': product.product.name,
            'quantity': product.quantity,
            'price':product.price,
            'image': product.image.url,
            'brand':product.brand,
            'id':product.id,

        })

    # Return the filtered products as JSON response
    return JsonResponse(products_data, safe=False)

def search_product(request):
    query = request.GET.get('search', '')
    products = Varient.objects.select_related('product').filter(product__name__icontains=query)

    results = []
    for product in products:
        results.append({
            'name': product.product.name,
            'quantity': product.quantity,
            'price':product.price,
            'image': product.image.url,
            'brand':product.brand,
            'id':product.id,

        })
    return JsonResponse({'results': results})

class UpdateProduct(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        print("update user")
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        obj = Product.objects.get(id=id1)
        obj.name = name1
        obj.save()
        print(obj)

        user = {'id': obj.id, 'name': obj.name}

        data = {
            'user': user
        }
        return JsonResponse(data)

    @csrf_exempt
    def post(self, request):
        form_id = request.POST.get('formId')
        form_name = request.POST.get('formName')

        try:
            product = Product.objects.get(id=form_id)
            product.name = form_name
            product.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.get(request, *args, **kwargs)
        elif request.method == 'POST':
            return self.post(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)
