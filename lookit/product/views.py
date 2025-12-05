import json
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Sum, Q, Value, Count
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from cloudinary.uploader import upload, destroy
from django.db.models import Case, When, Value, IntegerField

from .models import Style, Product, Variant, ProductImages
from cart.models import Cart

""" ============================================
    ADMIN SIDE
============================================ """

# custom decorator
def admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='/admin/login/',  # your custom login
    )(view_func)
    return decorated_view_func

@admin_required
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
        products = products.filter(category=category.lower())

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

@admin_required
def admin_add_product(request):
    if request.method == "POST":

        # ---retrive-all-post-data-------------------
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
        additional_images = request.FILES.getlist('additional_images')
        img_url = None
        image_public_id = None

        # --upload-image-to-cloudinary-----------------------------
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
            image_public_id = result['public_id']

        # ---create-new-product-
        product = Product.objects.create(
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
            image_public_id=image_public_id,
        )

        # ---upload-additional-images-------
        if additional_images:
            for file in additional_images:
                result = upload(
                    file,
                    folder=f"products/{product.name}/additional-images/",
                    transformation=[
                        {'width': 1080, 'height': 1080, 'crop': 'limit'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'},
                    ],
                )
                ProductImages.objects.create(
                    product=product,
                    image_url=result['secure_url'],
                    image_public_id=result['public_id'],
                )
        messages.success(request, "NEW PRODUCT CREATED")
        return redirect('admin-list-products')

    # ---redner-add-product-page------------------------------------------------
    styles = Style.objects.all()
    return render(request, "product/admin/add_product.html", {"styles": styles})

@admin_required
def admin_edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        # ---retrive-all-data
        name = request.POST.get('name').strip()
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

        main_image = request.FILES.get('image')
        image_public_id = product.image_public_id

        additional_images = request.FILES.getlist('additional_images')
        img_url = None

        # ---replace main image if changed--------------------------
        if main_image:
            if image_public_id != ' ':
                result = upload(
                    main_image,
                    folder=f"products/{name}/",
                    public_id=product.image_public_id,
                    overwrite=True,
                    transformation=[
                        {'width': 1080, 'height': 1080, 'crop': 'limit'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'},
                    ],
                )
                img_url = result.get('secure_url')
            # ---temporary else block to set image public id for products which have it empty
            else:
                result = upload(
                    main_image,
                    folder=f"products/{name}/",
                    transformation=[
                        {'width': 1080, 'height': 1080, 'crop': 'limit'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'},
                    ],
                )
                image_public_id = result['public_id']
                img_url = result.get('secure_url')
        else:
            img_url = request.POST.get('old_image_url')

        # ---manage-additional-images using hidden input( delete if missing)-----
        current_additional_images = ProductImages.objects.filter(product=product)
        for current_img in current_additional_images:
            # If hidden input is missing => image removed in UI
            if not request.POST.get(str(current_img.id)):
                print(current_img.id)
                # Remove from Cloudinary using public_id
                destroy(current_img.image_public_id)
                # Remove from db
                current_img.delete()

        # ---manage-additional-images( upload new ones )-------------------------
        if additional_images:
            for file in additional_images:
                result = upload(
                    file,
                    folder=f"products/{name}/additional-images/",
                    transformation=[
                        {'width': 1080, 'height': 1080, 'crop': 'limit'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'},
                    ],
                )
                ProductImages.objects.create(
                    product=product,
                    image_url=result['secure_url'],
                    image_public_id=result['public_id'],
                )
        # ---update-modal-----------------------------
        product = Product.objects.filter(id=product_id).update(
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
            image_public_id=image_public_id,
        )
        messages.success(request, f"PRODUCT DETAILS UPDATED")
        return redirect('admin-view-product', product_id=product_id)

    else:
        # ---prefill-and-render-edit-page--------------------------------
        additional_images = ProductImages.objects.filter(product=product)
        styles = Style.objects.all()
        return render(
            request,
            "product/admin/edit_product.html",
            {
                'product': product,
                'styles': styles,
                'additional_images': additional_images,
            },
        )


# --stock_management-------------------------
@admin_required
def admin_manage_stocks(request, product_id):
    product = (
        Product.objects.filter(id=product_id)
        .annotate(total_stock=Coalesce(Sum('variant__stock'), Value(0)))
        .first()
    )

    if request.method == "POST":
        size = request.POST.get('size')
        stock = request.POST.get('stock')

        size_already_exist = Variant.objects.filter(product=product, size=size).exists()
        if size_already_exist:
            messages.error(request, f"SIZE VARIANT ALREADY EXIST")
            return redirect('admin-manage-stocks', product_id=product_id)

        Variant.objects.create(product=product, size=size, stock=stock)
        messages.success(request, f"NEW VARIANT ADDED")
        return redirect('admin-manage-stocks', product_id=product_id)

    variants = Variant.objects.filter(product=product)
    return render(
        request,
        "product/admin/manage_stocks.html",
        {'product': product, 'variants': variants},
    )


# ---stock_update_ajax----------
@admin_required
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

@admin_required
def admin_delete_variant(request, variant_id):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        variant = Variant.objects.get(id=variant_id)
        variant.stock=0
        variant.save()
        messages.success(request, f"Size {variant.size} Stocks Removed")
        return redirect('admin-manage-stocks', product_id=product_id)

@admin_required
def admin_view_product(request, product_id):
    product = (
        Product.objects.filter(id=product_id)
        .annotate(
            total_stocks=Coalesce(Sum('variant__stock'), Value(0)),
            total_variants=Coalesce(Count('variant'), Value(0)),
        )
        .first()
    )
    product_images = ProductImages.objects.filter(product__id=product_id)
    return render(
        request,
        "product/admin/view_product.html",
        {"product": product, "product_images": product_images},
    )


def admin_toggle_product_active(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_active = not product.is_active
    product.save()
    print(product.is_active)
    if product.is_active:
        messages.success(request, f"PRODUCT RESTORED")
    else:
        messages.success(request, f"PRODUCT DELETED")
    return redirect('admin-view-product', product_id=product_id)

@admin_required
def admin_list_categories(request):
    styles = Style.objects.all()

    # pagination
    paginator = Paginator(styles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'product/admin/list_categories.html', {"page_obj": page_obj})

@admin_required
def admin_add_style(request):
    if request.method == "POST":
        style_name = request.POST.get('style_name').strip()
        print(f"request came with {style_name}")
        is_style_exist = Style.objects.filter(name__iexact=style_name).exists()
        if is_style_exist:
            messages.error(request, "Style already exist")
            return redirect('admin-category-management')
        style = Style.objects.create(name=style_name)
        messages.success(request, f"CREATED NEW STYLE - {style.name}")
    return redirect('admin-category-management')

@admin_required
def admin_search_categories(request):
    search_key = request.GET.get('search', '')
    search_result = Style.objects.filter(name__icontains=search_key)
    return render(
        request, 'product/admin/list_categories.html', {"page_obj": search_result}
    )

@admin_required
def admin_delete_category(request, style_id):
    style = Style.objects.get(id=style_id)
    style.is_deleted = True
    style.save()
    messages.success(request, f"STYLE DELETED - {style.name}")
    return redirect('admin-category-management')

@admin_required
def admin_restore_category(request, style_id):
    style = Style.objects.get(id=style_id)
    style.is_deleted = False
    style.save()
    messages.success(request, f"Restored style - {style.name}")
    return redirect('admin-category-management')

@admin_required
def admin_edit_category(request):
    if request.method == "POST":
        style_id = request.POST.get('style_id')
        style_name = request.POST.get('style_name').strip()

        style = Style.objects.get(id=style_id)
        style.name = style_name
        style.save()
        messages.success(request, f"EDITED STYLE - {style.name}")
        return redirect('admin-category-management')


""" ============================================
    USER SIDE
============================================ """


def explore(request):
    # fetch only products which are active and not out of stock
    products = Product.objects.filter(is_active=True, variant__stock__gt=0).distinct()
    # fetch only styles with minimum one product with minimum one stock
    styles = Style.objects.filter(product__variant__stock__gt=0).distinct()

    # ---category page
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category.lower())
        # fetch only styles which have atleast one product in men's category
        styles = styles.filter(product__category=category.lower()).distinct()

    # ---search----------------------------
    search_key = request.GET.get('search')
    if search_key:
        products = products.filter(name__icontains=search_key)

    # ---sort----------------------
    sort_name = request.GET.get('sort_name')
    sort_price = request.GET.get('sort_price')
    order_fields = []
    if sort_price:
        order_fields.append(sort_price)
    if sort_name:
        order_fields.append(sort_name)
    # if both sort exists first order by price then name
    products = products.order_by(*order_fields)

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


def product_details(request, product_uuid):
    #--fetch product----------------------------
    product = (
        Product.objects.filter(uuid=product_uuid)
        .annotate(
            total_stock=Coalesce(Sum('variant__stock'), 0),
            total_additional_images=Coalesce(Count('productimages'), 0),
        )
        .first()
    )

    # ---manual ordering for sizes----
    size_order = Case(
        When(size='S', then=Value(1)),
        When(size='M', then=Value(2)),
        When(size='L', then=Value(3)),
        When(size='XL', then=Value(4)),
        When(size='XXL', then=Value(5)),
        default=Value(99),
        output_field=IntegerField(),
    )
    # ---fetch all available sizes of this product-----------------------
    variants = Variant.objects.filter(product=product).order_by(size_order)

    # ---redirect to product listing page if product is not active-------
    if not product.is_active:
        messages.error(request, "PRODUCT IS UNAVAILABLE")
        return redirect('explore')

    # ---fetch additional product images--------------------------
    product_images = ProductImages.objects.filter(product=product)
    
    #---fetch related products---------------------------------------------------------------
    related_products = Product.objects.filter(category=product.category,is_active=True, variant__stock__gt=0).distinct().exclude(id=product.id)

    # ---old price for showing offer temporarly---
    old_price = int(product.price) * 1.2

    return render(
        request,
        "product/user/product_details.html",
        {
            "product": product,
            'old_price': old_price,
            'additional_product_images': product_images,
            'variants': variants,
            "related_products": related_products,
        },
    )


def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id')
        qunatity = request.POST.get('quantity')
        product = Product.objects.get(id=product_id)
        
        #restrict if not authenticated
        if not user.is_authenticated:
            messages.error(request, f"PLEASE LOG IN TO USE CART, id = {variant_id}")
            return redirect('product-details', product_uuid = product.uuid)
        
        #if size not selected
        if not variant_id:
            messages.error(request, "PLEASE SELECT A SIZE")
            return redirect('product-details', product_uuid = product.uuid)
        
        #check if product is active
        if not product.is_active:
            messages.error(request, "Product Is Currently Unavailble")
            return redirect('explore')
        
        is_already_exist = Cart.objects.filter(user=user, variant_id=variant_id)
        if is_already_exist:
            messages.error(request, "PRODUCT IS ALREADY IN CART")
            return redirect('product-details', product_uuid = product.uuid)
        
        #--stock validation---
        stock_mismatch = None
        variant = Variant.objects.get(id=variant_id)
        if int(variant.stock) == 0:
            messages.error(request, "")
            return redirect('product-details', product_uuid = product.uuid)
        elif int(variant.stock) < int(qunatity):
            stock_mismatch = f"Product Added to Cart. (note: only {variant.stock} stocks are available.)"
            qunatity = variant.stock
        
        try:
            Cart.objects.create(user=user, variant_id=variant_id, quantity=qunatity)
            if stock_mismatch:
                messages.success(request, stock_mismatch)
            else:
                messages.success(request, "Product Added to Cart")
        except Exception as e:
            print(e)
            messages.error(request, e)
            
    return redirect('product-details', product_uuid = product.uuid)