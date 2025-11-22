import json
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Sum, Q, Value, Count
from django.db.models.functions import Coalesce
from cloudinary.uploader import upload

from .models import Style, Product, Variant

""" ============================================
    ADMIN SIDE
============================================ """


def admin_list_products(request):
    products = Product.objects.annotate(
        total_stock=Coalesce(Sum('variant__stock'), Value(0))
    ).order_by('-is_active', '-created_at')
    styles = Style.objects.all()

    search = request.GET.get('search')
    category = request.GET.get('category')
    style = request.GET.get('style')
    stock_status = request.GET.get('stock')
    price_range = request.GET.get('price')

    if search:
        products = products.filter(name__icontains=search)

    if style:
        products = products.filter(style__name=style)

    if category:
        products = products.filter(category=category.upper())

    if stock_status:
        reorder_level = 30
        if stock_status == 'in_stock':
            products = products.filter(total_stock__gt=reorder_level)
        elif stock_status == 'low_stock':
            products = products.filter(total_stock__range=(1, reorder_level))
        elif stock_status == 'out_of_stock':
            products = products.filter(Q(total_stock=0) | Q(total_stock=None))

    if price_range:
        if '-' in price_range:
            min_price, max_price = price_range.split('-')
            products = products.filter(price__range=(min_price, max_price))
        elif "+" in price_range:
            min_price = price_range.split('+')[0]
            products = products.filter(price__gte=min_price)

    # pagination
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, "product/admin/list.html", {"page_obj": page_obj, "styles": styles}
    )


def admin_add_product(request):
    if request.method == "POST":

        name = request.POST.get('name')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        base_color = request.POST.get('base_color')
        category = request.POST.get('category')

        style_name = request.POST.get('style')
        style = Style.objects.get(name=style_name)

        material = request.POST.get('material')
        fit = request.POST.get('fit')
        care_instructions = request.POST.get('care_instructions')

        price = request.POST.get('price')

        image = request.FILES.get('image')
        img_url = None
        if image:
            result = upload(
                image,
                folder=f"products/{name}/",
                transformation=[
                    {'width': 1080, 'height': 1080, 'crop': 'limit'},
                    {'quality': 'auto'},
                    {'fetch_format': 'auto'},
                ],
            )
            img_url = result.get('secure_url')

        Product.objects.create(
            name=name,
            description=description,
            brand=brand,
            base_color=base_color,
            category=category.lower(),
            style=style,
            material=material,
            fit=fit,
            care_instructions=care_instructions,
            price=price,
            image_url=img_url,
        )

    styles = Style.objects.all()
    return render(request, "product/admin/add_product.html", {"styles": styles})


def admin_edit_product(request, product_id):
    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        base_color = request.POST.get('base_color')
        category = request.POST.get('category')

        style_name = request.POST.get('style')
        style = Style.objects.get(name=style_name)

        material = request.POST.get('material')
        fit = request.POST.get('fit')
        care_instructions = request.POST.get('care_instructions')
        price = request.POST.get('price')

        image = request.FILES.get('image')
        img_url = None
        if image:
            print(image)
            result = upload(
                image,
                folder=f"products/{name}/",
                transformation=[
                    {'width': 1080, 'height': 1080, 'crop': 'limit'},
                    {'quality': 'auto'},
                    {'fetch_format': 'auto'},
                ],
            )
            img_url = result.get('secure_url')
        print(image)

        Product.objects.filter(id=product_id).update(
            name=name,
            description=description,
            brand=brand,
            base_color=base_color,
            category=category.lower(),
            style=style,
            material=material,
            fit=fit,
            care_instructions=care_instructions,
            price=price,
            image_url=img_url,
        )
        return redirect('admin-view-product', product_id=product_id)

    product = Product.objects.get(id=product_id)
    styles = Style.objects.all()
    return render(
        request,
        "product/admin/edit_product.html",
        {'product': product, 'styles': styles},
    )


# --stock_management-------------------------
def admin_manage_stocks(request, product_id):
    product = (
        Product.objects.filter(id=product_id)
        .annotate(total_stock=Coalesce(Sum('variant__stock'), Value(0)))
        .first()
    )

    if request.method == "POST":
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        Variant.objects.create(product=product, size=size, stock=stock)
        return redirect('admin-manage-stocks', product_id=product_id)

    variants = Variant.objects.filter(product=product)
    return render(
        request,
        "product/admin/manage_stocks.html",
        {'product': product, 'variants': variants},
    )


# ---stock_update_ajax----------
def admin_update_stock(request):
    if request.method == "POST":
        # convert json data into python dict
        data = json.loads(request.body)

        variant_id = data.get('variant_id')
        new_stock = data.get('stock')

        # update new stock
        variant = Variant.objects.get(id=variant_id)
        variant.stock = new_stock
        variant.save()

    return JsonResponse(
        {"status": "success", "message": "Stock updated", "new_stock": new_stock}
    )


def admin_delete_variant(request, variant_id):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        Variant.objects.get(id=variant_id).delete()
        return redirect('admin-manage-stocks', product_id=product_id)


def admin_view_product(request, product_id):
    product = (
        Product.objects.filter(id=product_id)
        .annotate(
            total_stocks=Coalesce(Sum('variant__stock'), Value(0)),
            total_variants=Coalesce(Count('variant'), Value(0)),
        )
        .first()
    )
    return render(request, "product/admin/view_product.html", {"product": product})


def admin_toggle_product_active(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_active = not product.is_active
    product.save()
    print(product.is_active)
    return redirect('admin-view-product', product_id=product_id)


def admin_list_categories(request):
    styles = Style.objects.all()

    # pagination
    paginator = Paginator(styles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/admin/list_categories.html', {"page_obj": page_obj})


def admin_add_style(request):
    if request.method == "POST":
        style_name = request.POST.get('style_name').strip()
        print(f"request came with {style_name}")
        Style.objects.create(name=style_name)
    return redirect('admin-category-management')


def admin_search_categories(request):
    search_key = request.GET.get('search', '')
    search_result = Style.objects.filter(name__icontains=search_key)
    return render(
        request, 'product/admin/list_categories.html', {"page_obj": search_result}
    )


def admin_delete_category(request, style_id):
    style = Style.objects.get(id=style_id)
    style.is_deleted = True
    style.save()
    return redirect('admin-category-management')


def admin_restore_category(request, style_id):
    style = Style.objects.get(id=style_id)
    style.is_deleted = False
    style.save()
    return redirect('admin-category-management')


def admin_edit_category(request):
    if request.method == "POST":
        style_id = request.POST.get('style_id')
        style_name = request.POST.get('style_name').strip()

        style = Style.objects.get(id=style_id)
        style.name = style_name
        style.save()

        return redirect('admin-category-management')


""" ============================================
    USER SIDE
============================================ """


def explore(request):
    products = Product.objects.all()
    styles = Style.objects.all()

    # ---category page
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category.upper())

    # ---search----------------------------
    search_key = request.GET.get('search')
    if search_key:
        products = products.filter(name__icontains=search_key)

    # ---sort----------------------
    sort = request.GET.get('sort')
    if sort:
        if "price" in sort:
            products = products.order_by(sort)
        elif "name" in sort:
            products = products.order_by(sort)

    # ----filter---------------------
    style = request.GET.get('style')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    color = request.GET.get('color')
    size = request.GET.get('size')
    if style:
        products = products.filter(style__name__icontains=style)
    if price_min and price_max:
        products = products.filter(price__range=(price_min, price_max))
    if color:
        products = products.filter(base_color=color)
    if size:
        products = products.filter(variant__size=size.upper())

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(
        request, "product/user/explore.html", {"page_obj": page_obj, "styles": styles}
    )


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    old_price = int(product.price) * 1.2
    return render(
        request,
        "product/user/product_details.html",
        {"product": product, old_price: old_price},
    )
