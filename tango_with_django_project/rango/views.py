from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context_dict ={}
    context_dict['boldmessage'] = { 'Crunchy, creamy, cookie, candy, cupcake!'}
    context_dict['categories'] = categories
    context_dict['pages'] = pages
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response =  render(request, 'rango/index.html', context=context_dict)
    return response
    

def about(request):
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', {})

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

@login_required
def add_category(request):
    form = CategoryForm() 
    if request.method == 'POST':  
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    if category is None:
        return redirect('/rango/')
    
    form = PageForm() 
    if request.method == 'POST':  
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)# save a copy of the form in a variable page but don't saave to the db yet
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',
                                    kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    return render(request, 'rango/add_page.html', {'form': form, 'category':category})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST) # creates a form object and fills it with the data entered by the user
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() #user is a new form object, save method saves the form object into the database and the object
            #saved is now stored in the user object. we store it in another object to be able to change the password later.

            user.set_password(user.password) #hashes the plain password
            user.save() #saves the object again.

            profile = profile_form.save(commit=False)
            profile.user = user

            # Q: why do we have seperated models and forms for user and userProfile? 
            # A: because we already have a predefined user model in django that handles passwords and usernames
            # and we need another one to handle other information.

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture'] # if the user provided a picture replace the existing one with the new one.
            
            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                    'rango/register.html',
                    context = { 'user_form' : user_form,
                                'profile_form' : profile_form,
                                'registered' : registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # there might be an account for this person but has bee deactivated.
            if user.is_active:
                login(request,user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits','1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit' ,str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits