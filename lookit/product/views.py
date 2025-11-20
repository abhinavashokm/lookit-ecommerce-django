from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Style

""" ============================================
    ADMIN SIDE
============================================ """


def admin_list_products(request):
    return render(request, "product/admin/list.html")


def admin_add_product(request):
    return render(request, "product/admin/add_product.html")


def admin_add_variant(request):
    return render(request, "product/admin/add_variant.html")


def admin_list_variants(request):
    return render(request, "product/admin/list_variants.html")


def admin_list_categories(request):
    styles = Style.objects.all()
    
    #pagination
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
