from django.shortcuts import render

# Create your views here.
def admin_list_offers(request):
    return render(request, 'offer/list.html')

def admin_add_offer(request):
    return render(request, 'offer/add_offer.html')