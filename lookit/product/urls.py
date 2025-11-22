from django.urls import path
from .views import (
    admin_list_products,
    admin_add_product,
    admin_list_categories,
    admin_add_style,
    admin_search_categories,
    admin_delete_category,
    admin_restore_category,
    admin_edit_category,
    admin_view_product,
    admin_manage_stocks,
    admin_update_stock,
    admin_delete_variant,
    
    product_details,
    explore,
)

urlpatterns = [
    path("admin/list/", admin_list_products, name="admin-list-products"),
    path("admin/add-product/", admin_add_product, name="admin-add-product"),
    path("admin/view-product/<product_id>", admin_view_product, name="admin-view-product"),
    path("admin/manage-stocks/<product_id>", admin_manage_stocks, name="admin-manage-stocks"),
    path("admin/update-stocks", admin_update_stock, name="admin-update-stock"),
    path("admin/delete_variant/<variant_id>", admin_delete_variant, name="admin-delete-variant"),
    
    path(
        "admin/category/list",
        admin_list_categories,
        name='admin-category-management',
    ),
    path("admin/category/add-style", admin_add_style, name="admin-add-style"),
    path("admin/category/search-categories", admin_search_categories, name="admin-search-categories"),
    path("admin/category/delete-style/<style_id>", admin_delete_category, name="admin-delete-category"),
    path("admin/category/restore-style/<style_id>", admin_restore_category, name="admin-restore-category"),
    path("admin/category/edit-style/", admin_edit_category, name="admin-edit-category"),
    
    path("product-details/<product_id>/",product_details, name="product-details"),
    path("explore/", explore, name="explore"),
    

]
