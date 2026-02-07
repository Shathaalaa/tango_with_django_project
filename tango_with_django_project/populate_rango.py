import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE'
,'tango_with_django_project.settings')
import django
django.setup()
from rango.models import Category, Page

def populate():
    python_pages = [
    {'title': 'Official Python Tutorial',
     'url':'http://docs.python.org/3/tutorial/',
    'views':90},

    {'title':'How to Think like a Computer Scientist',
    'url':'http://www.greenteapress.com/thinkpython/',
    'views':70},

    {'title':'Learn Python in 10 Minutes',
     'url':'http://www.korokithakis.net/tutorials/python/',
     'views':20} 
    ] 

    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
        'views':30},
        
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        'views':33},

        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        'views':50} 
    ]

    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/',
        'views':30},
        

        {'title':'Flask',
        'url':'http://flask.pocoo.org',
        'views':11} 
    ]

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes':64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views':32, 'likes':16}, 
    }

    for cat, catPages in cats.items():
        c = addCat(cat, catPages['views'], catPages['likes'] ) 
        for page in catPages['pages']:
            addPage(c, page['title'], page['url'], page['views'])

    
    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print(f'- {c}: {p}')

def addCat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name = name)[0]
    c.views = views
    c.likes = likes
    c.save() 
    return(c)

def addPage(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category = cat, title= title)[0]# these two are only used for lookup
    p.url = url 
    p.views = views 
    p.save() 
    return(p)

if __name__ == '__main__': # this means we can run the file by calling python populate-rango.py
    # and it also means that when this class is imported it won't be imported with it
    print('Starting Rango population script...')
    populate()