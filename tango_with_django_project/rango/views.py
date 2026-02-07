from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page



def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context_dict ={}
    context_dict['boldmessage'] = { 'Crunchy, creamy, cookie, candy, cupcake!'}
    context_dict['categories'] = categories
    context_dict['pages'] = pages
    return render(request, 'rango/index.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict ={}
    try:
        category = Category.objects.get(slug = category_name_slug)
        pages = Page.objects.filter(category = category)
        context_dict ={}
        context_dict['pages'] = pages
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context = context_dict)
