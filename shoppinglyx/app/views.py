from django.shortcuts import render, redirect, HttpResponse
from django.views import View  # to create class bassed view Imported View class
from .models import Customer, Product, Cart, OrderPlaced  # imprted all the models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
import razorpay
from django.conf import settings

# def home(request):
#  return render(request, 'app/home.html')

# Create class bassed view for home


class ProductView(View):
    def get(self, request):
        # is it from our model Product where our category_choise is defined and catogory field as well
        topwears = Product.objects.filter(category="TW")
        bottomwears = Product.objects.filter(category="BW")
        mobiles = Product.objects.filter(category="M")
        laptops = Product.objects.filter(category="L")

        return render(
            request,
            "app/home.html",
            {
                "topwears": topwears,
                "bottomwears": bottomwears,
                "mobiles": mobiles,
                "laptops": laptops,
            },
        )


# def product_detail(request):
#     return render(request, "app/productdetail.html")


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_in_cart = False
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(
                Q(product=product) & Q(user=request.user)
            ).exists()

        return render(
            request,
            "app/productdetail.html",
            {"product": product, "item_in_cart": item_in_cart},
        )


def topwear(request):
    topwears = Product.objects.filter(category="TW")
    return render(request, "app/topwear.html", {"topwears": topwears})


def bottomwear(request):
    bottomwears = Product.objects.filter(category="BW")
    return render(request, "app/bottomwear.html", {"bottomwears": bottomwears})


def laptop(request):
    laptops = Product.objects.filter(category="L")
    return render(request, "app/laptop.html", {"laptops": laptops})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod-id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)

        if cart_product:
            for p in cart_product:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount
            total_amount = amount + shipping_amount

        return render(
            request,
            "app/addtocart.html",
            {"carts": cart, "totalamount": total_amount, "amount": amount},
        )
    else:
        return render(request, "app/emptycart.html")


# for quantity on cart page used Ajax


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "totalamount": amount + shipping_amount,
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount

        data = {
            "quantity": c.quantity,
            "amount": amount,
            "totalamount": amount + shipping_amount,
        }
        return JsonResponse(data)


def remove_cart_item(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount

        data = {"amount": amount, "totalamount": amount + shipping_amount}
        return JsonResponse(data)


@login_required
# def payment_done(request):
#     user = request.user
#     # transaction_id = request.GET.get("paypal_paymnet_id")
#     transaction_id = request.GET.get("razorpay_payment_id")
#     transaction_id_paypal = request.GET.get("paypal-payment-id")
#     custid = request.GET.get("custid")
#     customer = Customer.objects.get(id=custid)
#     cart_item = Cart.objects.filter(user=user)
#     print("Razorpay")
#     print(transaction_id)
#     for cart in cart_item:
#         OrderPlaced(
#             user=user,
#             customer=customer,
#             product=cart.product,
#             quantity=cart.quantity,
#             transaction_id=transaction_id,
#         ).save()
#         cart.delete()
#     print("Paypalid")
#     print(transaction_id_paypal)
#     return redirect("orders")


def payment_done(request):
    user = request.user
    razor_transaction_id = request.GET.get("razorpay_payment_id")
    paypal_transaction_id = request.GET.get("paypal-payment-id")
    custid = request.GET.get("custid")
    customer = Customer.objects.get(id=custid)
    cart_items = Cart.objects.filter(user=user)

    print(razor_transaction_id)
    print(paypal_transaction_id)

    # Check if the payment was made with Razorpay
    if razor_transaction_id:
        for cart in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=cart.product,
                quantity=cart.quantity,
                transaction_id=razor_transaction_id,
            )
            cart.delete()
        return redirect("orders")

    # Check if the payment was made with PayPal
    elif paypal_transaction_id:
        for cart in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=cart.product,
                quantity=cart.quantity,
                transaction_id=paypal_transaction_id,
            )
            cart.delete()

        return redirect("orders")

    # Handle the case where neither Razorpay nor PayPal payment ID is provided
    else:
        return HttpResponse("Invalid payment information")


def payment_success(request):
    return render(request, "payment_success.html")


def payment_failed(request):
    return render(request, "payment_failed.html")


def buy_now(request):
    return render(request, "app/buynow.html")


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", {"add": add, "active": "btn-primary"})


@login_required
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, "app/orders.html", {"order_placed": order_placed})


def mobile(request, data=None):
    # For filter the mobile, by brand and price
    if data == None:
        mobiles = Product.objects.filter(category="M")

    elif data == "Redmi" or data == "Apple":
        mobiles = Product.objects.filter(category="M").filter(
            brand=data
        )  # in urls.py used with mobiledata name path
    elif data == "below":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__lt=10000
        )  # ye ek filter method he(lt = less than)
    elif data == "above":
        mobiles = Product.objects.filter(category="M").filter(
            discounted_price__gt=10000
        )

    return render(request, "app/mobile.html", {"mobiles": mobiles})


# for this we will not create any view we can directly bcz we are using django default authentication we can write it in url and can access it

# def login_page(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         user = authenticate(username=username, password=password)
#         if user:
#             login(
#                 request, user
#             )  # yha pr vo login kr dega or session me value dal denge login ke throgh
#             return redirect("/")
#         else:
#             # Handle invalid login
#             messages.error(request, "Invalid Username or Password")
#             return redirect("/login/")

#     return render(request, "app/login.html")


# def customerregistration(request):
#     if request.method == "POST":
#         # Extract form data
#         first_name = request.POST["first_name"]
#         last_name = request.POST["last_name"]
#         email = request.POST["email"]
#         username = request.POST["username"]
#         password = request.POST["password"]
#         confirm_password = request.POST["confirm_password"]

#         print("this is testing")
#         if password == confirm_password:
#             # Check if the username is already taken
#             user_exists = User.objects.filter(username=username).first()
#             print("this is the msg", user_exists)
#             if user_exists:
#                 print("User exists")
#                 # Handle username already exists error
#                 messages.error(request, "Username already exists.")
#                 return redirect("/registration/")  # Redirect to the register page

#                 # Create a new user
#             else:
#                 print("data coming")
#                 user = User.objects.create_user(
#                     first_name=first_name,
#                     last_name=last_name,
#                     username=username,
#                     email=email,
#                 )
#                 user.set_password(password)  # Encrypt the password
#                 user.save()
#                 messages.success(request, "Account created successfully!")

#                 # Log the user in and redirect to a different page
#                 login(request, user)
#                 return redirect("/")
#         else:
#             messages.error(request, "Both Passwords are matching.")
#             return redirect("/registration/")

#     return render(request, "app/customerregistration.html")


class CustomerRegistrationView(View):
    def get(self, request):  # for get request, when click or heat the register url
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {"form": form})

    def post(self, request):
        # Check if the username is already taken
        form = CustomerRegistrationForm(request.POST)
        username = request.POST["username"]
        user_exists = User.objects.filter(username=username).first()
        if user_exists:
            # Handle username already exists error
            messages.error(request, "Username already exists.")
            return redirect("/registration/")  # Redirect to the register page

        elif form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
        return render(request, "app/customerregistration.html", {"form": form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    if cart_product:

        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
            total_amount = amount + shipping_amount

    return render(
        request,
        "app/checkout.html",
        {"add": add, "total_amount": total_amount, "cart_items": cart_items},
    )


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(
            request, "app/profile.html", {"form": form, "active": "btn-primary"}
        )

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            data = Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode,
            )
            data.save()
            messages.success(request, "Congratulations!! Profile Updated Successfully")
            return render(
                request, "app/profile.html", {"form": form, "active": "btn-primary"}
            )


#  Search functinality


# def search(request):
#     query = request.GET["query"]
#     if len(query) > 80:
#         allproducts = Product.objects.none()
#     else:
#         allproductsTitle = Product.objects.filter(title__icontains=query)
#         allproductsBrand = Product.objects.filter(brand__icontains=query)
#         allproducts = allproductsTitle.union(allproductsBrand)
#     if allproducts.count() == 0:
#         messages.warning(request, "No search results found. Please refine your query.")

#     return render(
#         request, "app/search.html", {"allproducts": allproducts, "query": query}
#     )


# def search(request):
#     query = request.GET.get("query", "")
#     if not query:
#         allproducts = Product.objects.none()
#     else:
#         allproducts = Product.objects.filter(
#             Q(title__icontains=query) | Q(brand__icontains=query)
#         )

#     if allproducts.count() == 0:
#         messages.warning(request, "No search results found. Please refine your query.")

#     context = {
#         "allproducts": allproducts,
#         "query": query,
#     }

#     if allproducts.count() == 0:
#         context["no_results"] = True

#     return render(request, "app/search.html", context)


def search(request):
    query = request.GET.get("query", "")
    allproducts = Product.objects.none()

    if query:
        allproducts = Product.objects.filter(
            Q(title__icontains=query) | Q(brand__icontains=query)
        )

    if allproducts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")

    context = {
        "allproducts": allproducts,
        "query": query,
        "no_results": allproducts.count() == 0,
    }

    return render(request, "app/search.html", context)


# Razorpay paymnet


# def initiate_payment(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         amount = request.POST.get("amount")
#         client = razorpay.Client(
#             auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
#         )
#         razorpay_order = client.order.create(
#             {"amount": str(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         )
#         order = OrderPlaced.objects.create(
#             name=name, amount=amount, provider_order_id=["id"]
#         )
#         order.save()
#         return render(
#             request,
#             "payment.html",
#             {
#                 "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
#                 "razorpay_key": settings.RAZORPAY_KEY_ID,
#                 "order": order,
#             },
#         )
#     return render(request, "orders.html")

# if request.method == "POST":
#     client = razorpay.Client(
#         auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
#     )
#     paymnet = client.order.create(
#         {"amount": Cart.total_cost, "currency": "INR", "payment_capture": "1"}
#     )

#     print("****************")
#     print(paymnet)
#     print("****************")

#     context = {"cart": Cart.total_cost, "payment": paymnet}
