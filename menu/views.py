from django.shortcuts import render
from django.db.models import Avg
from .models import MenuItem, Category


def menu_list(request):

    items = MenuItem.objects.all()
    categories = Category.objects.all()

    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        items = items.filter(
            category__name=category
        )

    if search:
        items = items.filter(
            name__icontains=search
        )

    # Add review stats to each food item
    for item in items:

        item.avg_rating = item.reviews.aggregate(
            Avg('rating')
        )['rating__avg']

        item.review_count = item.reviews.count()

    context = {
        'items': items,
        'categories': categories,
        'item_count': items.count(),
        'category_count': categories.count(),
    }

    return render(
        request,
        'menu/menu.html',
        context
    )

# from django.shortcuts import render
# from .models import MenuItem, Category
# 
# def menu_list(request):
# 
#     items = MenuItem.objects.all()
#     categories = Category.objects.all()
# 
#     category = request.GET.get('category')
#     search = request.GET.get('search')
# 
#     if category:
#         items = items.filter(category__name=category)
# 
#     if search:
#         items = items.filter(name__icontains=search)
# 
#     context = {
#         'items': items,
#         'categories': categories,
#         'item_count': items.count(),
#         'category_count': categories.count(),
#     }
# 
#     return render(request, 'menu/menu.html', context)