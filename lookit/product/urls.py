from django.urls import path
from .views import admin_list_products, admin_add_product, admin_add_variant, admin_list_variants, admin_category_management

urlpatterns = [
    path("admin/list/", admin_list_products, name="admin-list-products"),
    path("admin/add-product/", admin_add_product, name="admin-add-product"),
    path("admin/add-variant/", admin_add_variant, name="admin-add-variant"),
    path("admin/list-variants/", admin_list_variants, name="admin-list-variants"),
    path("admin/category-management", admin_category_management, name='admin-category-management'),
]