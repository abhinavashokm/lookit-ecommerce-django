from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from product.models import Style
from offer.models import Offer


# Create your views here.
def admin_list_offers(request):
    offers = Offer.objects.all()
    
    #--create pagination object-----
    paginator = Paginator(offers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'offer/list.html',{'page_obj':page_obj})


def admin_add_offer(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        scope = request.POST.get('scope', '').strip()

        style_name = request.POST.get('style', '').strip()
        selected_products = request.POST.getlist('selected_products')

        discount = request.POST.get('discount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        status = request.POST.get('status')
        is_active = True if status == 'on' else False

        # Required fields dictionary
        required_fields = {
            "Offer Name": name,
            "Scope": scope,
            "Discount Percentage": discount,
            "Start Date": start_date,
            "End Date": end_date,
        }

        # -- Required field vaidation ----------------------------------------------------
        missing_fields = [
            field for field, value in required_fields.items() if not value
        ]
        if missing_fields:
            messages.error(
                request, "Missing required fields: " + ", ".join(missing_fields)
            )
            return redirect('admin-add-offer')

        if scope == 'category':
            try:
                style = Style.objects.get(name=style_name)
                Offer.objects.create(
                    name=name,
                    scope=Offer.Scopes.CATEGORY_BASED,
                    style=style,
                    discount=discount,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=is_active,
                )
                messages.success(request, "Offer Created Successfully")
                print(request.POST)
                return redirect('admin-list-offers')
            except Exception as e:
                print(e)
                messages.error(request, "Something went wrong")
                return redirect('admin-add-offer')
                
        elif scope == 'product':
            messages.error(request, "Product Based Offer Is Work In Progress")
            return redirect('admin-add-offer')

    styles = Style.objects.all()
    return render(request, 'offer/add_offer.html', {'styles': styles})
