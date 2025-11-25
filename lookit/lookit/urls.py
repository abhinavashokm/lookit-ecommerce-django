from django.urls import path, include

urlpatterns = [
    path("user/",include('user.urls')),
    path("",include('core.urls')),
    path("admin/", include('staff.urls')),
    path("product/", include('product.urls')),
    path("cart/", include('cart.urls')),
        # continue with google
    path('oauth/', include('social_django.urls', namespace='social')),
]
