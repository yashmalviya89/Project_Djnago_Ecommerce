from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import (
    LoginForm,
    MyPasswordChangeForm,
    MyPasswordResetForm,
    MySetPasswordForm,
)
from .views import (
    ProductView,
    ProductDetailView,
    mobile,
    topwear,
    bottomwear,
    laptop,
)


urlpatterns = [
    # path("", views.home),
    # We have created class based view so we'll define our url like this
    path("", views.ProductView.as_view(), name="home"),
    # path("product-detail/", views.product_detail, name="product-detail"),
    path(
        "product-detail/<int:pk>",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="showcart"),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removeitem/", views.remove_cart_item),
    path("checkout/", views.checkout, name="checkout"),
    path("paymentdone/", views.payment_done, name="paymentdone"),
    path("buy/", views.buy_now, name="buy-now"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("orders/", views.orders, name="orders"),
    path("", ProductView.as_view(), name="home"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("topwear/", topwear, name="topwear"),
    path("bottomwear/", bottomwear, name="bottomwear"),
    path("mobile/", views.mobile, name="mobile"),
    path("laptop/", laptop, name="laptop"),
    path("search", views.search, name="search"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
    path("mobile/<slug:data>", views.mobile, name="mobiledata"),  # for createing filter
    # for this we will not create any view we can directly bcz we are using django default authentication we can write it in url and can access it
    # path("login/", views.login_page, name="login"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="app/login.html",
            authentication_form=LoginForm,  # imported views for this auth_views
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    # path("registration/", views.customerregistration, name="customerregistration"),
    path(
        "registration/",
        views.CustomerRegistrationView.as_view(),
        name="customerregistration",
    ),
    path(
        "passwordchange/",
        auth_views.PasswordChangeView.as_view(
            template_name="app/passwordchange.html",
            form_class=MyPasswordChangeForm,
            success_url="/passwordchangedone/",
        ),
        name="passwordchange",
    ),
    path(
        "passwordchangedone/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="app/passwordchangedone.html"
        ),
        name="passwordchangedone",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="app/password_reset.html", form_class=MyPasswordResetForm
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="app/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="app/password_reset_confirm.html",
            form_class="MySetPasswordForm",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="app/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
