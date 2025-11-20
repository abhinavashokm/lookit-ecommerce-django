from django.urls import path
from .views import (
    admin_list_products,
    admin_add_product,
    admin_add_variant,
    admin_list_variants,
    admin_list_categories,
    admin_add_style,
    admin_search_categories,
    admin_delete_category,
    admin_restore_category,
    admin_edit_category,
    admin_view_product,
    admin_manage_stocks,
    admin_update_stock
)

urlpatterns = [
    path("admin/list/", admin_list_products, name="admin-list-products"),
    path("admin/add-product/", admin_add_product, name="admin-add-product"),
    path("admin/add-variant/", admin_add_variant, name="admin-add-variant"),
    path("admin/list-variants/", admin_list_variants, name="admin-list-variants"),
    path(
        "admin/category-management",
        admin_list_categories,
        name='admin-category-management',
    ),
    path("admin/add-style", admin_add_style, name="admin-add-style"),
    path("admin/search-categories", admin_search_categories, name="admin-search-categories"),
    path("admin/delete-category/<style_id>", admin_delete_category, name="admin-delete-category"),
    path("admin/restore-category/<style_id>", admin_restore_category, name="admin-restore-category"),
    path("admin/edit-category/", admin_edit_category, name="admin-edit-category"),
    path("admin/view-product/<product_id>", admin_view_product, name="admin-view-product"),
    path("admin/product/manage-stocks/<product_id>", admin_manage_stocks, name="admin-manage-stocks"),
    path("admin/product/update-stock", admin_update_stock, name="admin-update-stock")
]
