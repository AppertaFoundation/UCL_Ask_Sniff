""" The main part of the backend server """
from datetime import date
import platform
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.contrib.auth.models import Group
from django.db.models import Q
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from decouple import config
from requests import post as make_post_call
from requests import ConnectionError as RequestsConnectionError
from .models import Child, Category, Heading, SubHeading, DiaryLog, AgeGroup
from .forms import LoginForm, SignUpForm, AddChildForm, EditChildForm, SubHeadingEditForm, HeadingEditForm, CategoryEditForm, SearchForm,\
DiaryLogEditForm, ForgotPassword
from .decorators import disclaimer_required, admin_required, age_required

def index(request):
    """ the index page is the first page the user sees """
    name = platform.uname()[1]
    if request.user.is_authenticated() or request.session.has_key('age_range'):
        return redirect('homepage')
    login_form = LoginForm()
    signup_form = SignUpForm()
    next_redirect = request.GET.get('next', None)
    return render(request, 'index.html', {
        'loginForm': login_form,
        'signupForm':signup_form,
        'redirect':next_redirect,
        'name':name,
    })

@login_required
@admin_required
def all_urls(request):
    # pylint: disable=W0613
    """ return all the urls for the models so that admin can use them for hyperlinks in articles """
    results = cache.get("all_urls")
    if results is None:
        categories = Category.objects.all()
        headings = Heading.objects.all()
        sub_headings = SubHeading.objects.all()
        results = []
        for category in categories:
            url_info = {'name':'Symptom: ' + str(category), 'url': category.get_absolute_url()}
            results.append(url_info)
        for heading in headings:
            url_info = {'name':'Heading: ' + str(heading), 'url': heading.get_absolute_url()}
            results.append(url_info)
        for sub_heading in sub_headings:
            url_info = {'name':'Sub Heading: ' + str(sub_heading), 'url': sub_heading.get_absolute_url()}
            results.append(url_info)
        cache.set("all_urls", results, 60*15)
    return JsonResponse(results, safe=False)

@login_required
@disclaimer_required
@admin_required
def admin(request):
    """ the admin page contains the symptoms available in the website. Dashboard for the admin to make changes to the content of the website """
    form = CategoryEditForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        if 'edit' in request.POST:
            symptom_id = int(request.POST.get('id'))
            print(symptom_id)
            category = Category.objects.filter(categoryId=symptom_id).first()
            form = CategoryEditForm(request.POST, instance=category)
        else:
            form = CategoryEditForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('admin')
    symptoms_form = []
    for cat in categories:
        symptoms_form.append({"form":CategoryEditForm(instance=cat), "id":cat.categoryId})
    return render(request, 'admin.html', {
        'categories':categories,
        'form':form,
        'edit_symptoms':symptoms_form,
    })

@require_POST
@admin_required
def symptom_delete(request):
    """ delete a symptom using the admin panel """
    symptom_id = int(request.POST['id'])
    category_delete = Category.objects.filter(categoryId=symptom_id).first()
    category_delete.delete()
    return JsonResponse({'status':1, 'id':symptom_id})

@login_required
@disclaimer_required
@admin_required
def admin_symptom(request, symptom_name):
    """ admin can view all headings and subheading of a symptom, add a heading and subheading or edit an existing heading or subheading """
    symptom_name = symptom_name.lower()
    category = Category.objects.filter(categoryName=symptom_name).first()
    if category is None:
        try:
            category = Category.objects.filter(categoryId=symptom_name).first()
            if category is None:
                raise ValueError
        except ValueError:
            return redirect('admin')
    results = []
    headings = Heading.objects.filter(categoryName=category)
    for heading in headings:
        sub_headings = SubHeading.objects.filter(headingId=heading)
        results.append((heading, sub_headings))
    return render(request, 'admin_symptom.html', {
        'category':category,
        'results':results,
    })

@login_required
@disclaimer_required
@admin_required
def admin_headings(request, heading_id):
    """ admin can create a new heading or edit an existing heading """
    if request.method == 'POST':
        if 'delete' in request.POST:
            try:
                heading = Heading.objects.get(headingId=heading_id)
                heading.delete()
            except Heading.DoesNotExist:
                return redirect('admin')
            return redirect('admin_symptom', request.POST['categoryName'])
        heading_form = HeadingEditForm(request.POST)
        if heading_form.is_valid():
            try:
                heading = Heading.objects.get(headingId=heading_id)
                heading.categoryName = heading_form.cleaned_data['categoryName']
                heading.text = heading_form.cleaned_data['text']
                heading.save()
            except Heading.DoesNotExist:
                heading_form.save()
            return redirect('admin_symptom', heading_form.cleaned_data['categoryName'])
        return render(request, 'admin_heading.html', {
            'form':heading_form,
        })
    # id == 0 means we want to add a new heading. Else we are editing an already existing heading
    if int(heading_id) == 0:
        form = HeadingEditForm()
    else:
        heading = Heading.objects.filter(headingId=heading_id).first()
        if heading is None:
            return redirect('admin')
        form = HeadingEditForm(instance=heading)
    return render(request, 'admin_heading.html', {
        'form':form,
    })

@login_required
@disclaimer_required
@admin_required
def admin_subheadings(request, heading_id, sub_heading_id):
    # pylint: disable=R0911
    """ admin can create a new subheading or edit an existing subheading """
    new_sub_heading = True
    if request.method == 'POST':
        if 'delete' in request.POST:
            sub_heading = SubHeading.objects.filter(subHeadingId=sub_heading_id).first()
            if not sub_heading:
                return redirect('admin')
            sub_heading.delete()
            return redirect('admin_symptom', sub_heading.headingId.categoryName)
        sub_heading_form = SubHeadingEditForm(request.POST)
        sub_heading = SubHeading.objects.filter(subHeadingId=sub_heading_id).first()
        if sub_heading is not None:
            new_sub_heading = False
            sub_heading_form = SubHeadingEditForm(request.POST, instance=sub_heading)
        if sub_heading_form.is_valid():
            sub_heading_form.save()
            category = sub_heading_form.cleaned_data['headingId'].categoryName
            return redirect('admin_symptom', category)
        return render(request, 'admin_subheading.html', {
            'form':sub_heading_form,
            'new_sub_heading':new_sub_heading
        })
    # id == 0 means we want to add a new sub heading. Else we are editing an already existing subheading
    if int(sub_heading_id) == 0:
        heading = Heading.objects.filter(headingId=heading_id).first()
        if heading is None:
            return redirect('admin')
        sub_heading_form = SubHeadingEditForm(initial={'headingId':heading.headingId})
    else:
        sub_heading = SubHeading.objects.filter(subHeadingId=sub_heading_id).first()
        if sub_heading is None:
            return redirect('admin')
        new_sub_heading = False
        sub_heading_form = SubHeadingEditForm(instance=sub_heading)
    return render(request, 'admin_subheading.html', {
        'form':sub_heading_form,
        'new_sub_heading':new_sub_heading,
    })

def user_login(request):
    """ login processing. Successfull login is redirected disclaimer. """
    username = ''
    password = ''
    if request.method == 'POST':
        next_redirect = request.POST.get('redirect', None)
        login_form = LoginForm(request.POST)
        signup_form = SignUpForm()
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
        else:
            login_form = LoginForm()
            return render(request, 'index.html', {
                'loginForm':login_form,
                'signupForm':signup_form,
                'error':'Incorrect Username/Password'
            })

        login_form = LoginForm()
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'index.html', {
                'loginForm':login_form,
                'signupForm':signup_form,
                'error':'Incorrect Username'
            })

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next_redirect:
                return redirect(reverse('disclaimer') + "?next=" + next_redirect)
            return redirect('disclaimer')
        return render(request, 'index.html', {
            'loginForm':login_form,
            'signupForm':signup_form,
            'error':'Incorrect Password'
        })
    return redirect('index')

def user_signup(request):
    """ sign up processing. Successfull sign up is redirected disclaimer. """
    if request.method == 'POST':
        next_redirect = request.POST.get('redirect', None)
        login_form = LoginForm()
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            password = signup_form.cleaned_data['password']
            email = signup_form.cleaned_data['email']
        else:
            signup_form = SignUpForm()
            return render(request, 'index.html', {
                'loginForm':login_form,
                'signupForm':signup_form,
                'error':'Username Already exists'
            })
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            group = Group.objects.get(name='Users')
            user.groups.add(group)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if next_redirect:
                    return redirect(reverse('disclaimer') + "?next=" + next_redirect)
                return redirect('disclaimer')
            return render(request, 'index.html', {
                'loginForm':login_form,
                'signupForm':signup_form,
                'error':'Username Already exists'
            })
        except (IntegrityError, ValueError):
            signup_form = SignUpForm()
            return render(request, 'index.html', {
                'loginForm':login_form,
                'signupForm':signup_form,
                'error':'Username Already exists'
            })
    return redirect('index')

def forgot_password(request):
    """ view for resetting password if user has forgotten password """
    if request.method == "POST":
        forgot_form = ForgotPassword(request.POST)
        if forgot_form.is_valid():
            username = forgot_form.cleaned_data['username']
            password = forgot_form.cleaned_data['password']
            email = forgot_form.cleaned_data['email']
        else:
            return render(request, 'forgot_password.html', {
                'forgotForm':forgot_form,
                'error':"Error. Try again"
            })
        user = User.objects.filter(username=username, email=email).first()
        if user:
            user.set_password(password)
            user.save()
            return redirect('index')
        return render(request, 'forgot_password.html', {
            'forgotForm': forgot_form,
            'error': "Incorrect Username-Email combination"
        })
    form = ForgotPassword()
    return render(request, 'forgot_password.html', {
        'forgotForm':form,
    })
@disclaimer_required
@age_required
def homepage(request):
    """ the main home page after login or login skipped with age selected """
    symptoms = Category.objects.all()
    child_name = None
    child_age = None
    select_age = None
    if request.user.is_authenticated:
        child = Child.objects.filter(Q(username=request.user) & Q(activate=True))
        if child:
            child_name = child[0].childName
            child_age = get_age_string(child[0])
        else:
            return redirect('myChild')
    if request.session.has_key('age_range'):
        select_age = age_group_to_string(request.session['age_range'])
    return render(request, 'homepage.html', {
        'childName':child_name,
        'childAge':child_age,
        'selectedAge':select_age,
        'symptoms':symptoms
    })

def get_age_string(child_object):
    """ get a childs age in terms of months or years and months """
    child_age = child_object.dob
    child_months = ((date.today().year - child_age.year)*12) + (date.today().month - child_age.month)
    if child_months < 25:
        return str(child_months) + " months"
    years = round(child_months/12)
    month = child_months % 12
    return str(years) + " years and " + str(month) + " months"

def age_group_to_string(age_group):
    """ returns the string representation of an age group object """
    return str(AgeGroup.objects.get(age_group=age_group))


@disclaimer_required
def age(request):
    """ user who skips login is redirected here. User has to pick age to get relevant information """
    next_redirect = request.GET.get('next', None)
    if request.method == 'POST':
        age_range = request.POST.get('age', 0)
        request.session['disclaimer'] = True
        request.session['age_range'] = age_range
        if next_redirect:
            return redirect(next_redirect)
        return redirect('homepage')
    return render(request, 'age_select.html')

def disclaimer(request):
    """ the discalimer page. If user does not accept the terms they cannot use the website """
    next_redirect = request.GET.get('next', None)
    if request.session.has_key('age_range'):
        del request.session['age_range']
    if request.session.has_key('disclaimer'):
        del request.session['disclaimer']
    if request.method == 'POST':
        request.session['disclaimer'] = True
        if next_redirect:
            if request.user.is_authenticated:
                return redirect(next_redirect)
            return redirect(reverse('age') + "?next=" + next_redirect)
        elif request.user.is_authenticated:
            return redirect('homepage')
        return redirect('age')
    return render(request, 'disclaimer.html')

@disclaimer_required
@age_required
def symptom(request, symptom_name):
    """ the page produced for a symptom. Shows all the headings for that symptom """
    symptom_name = symptom_name.lower()
    headings = cache.get(symptom_name)
    description = cache.get(symptom_name + "_description")
    if description is None:
        category = Category.objects.filter(categoryName=symptom_name).first()
        description = None
        if category:
            description = category.description
            cache.set(symptom_name + "_description", description, 60*15)
    if headings is None:
        headings = Heading.objects.filter(categoryName=category)
        cache.set(symptom_name, headings, 60*15)
    child_name = None
    child_age = None
    select_age = None
    if request.user.is_authenticated:
        child = Child.objects.filter(Q(username=request.user) & Q(activate=True))
        if child:
            child_name = child[0].childName
            child_age = get_age_string(child[0])
        else:
            return redirect('myChild')
    if request.session.has_key('age_range'):
        select_age = age_group_to_string(request.session['age_range'])
    return render(request, 'symptom.html', {
        'symptom':symptom_name.replace('_', ' ').title(),
        'description':description,
        'headings':headings,
        'childName':child_name,
        'childAge':child_age,
        'selectedAge':select_age,
    })

@disclaimer_required
@age_required
def symptom_heading(request, heading_id):
    """ shows all the subheadings for a heading of a symptom """
    heading = Heading.objects.filter(headingId=heading_id).first()
    if request.user.is_authenticated:
        age_group = get_age_group(request)
        if age_group == 10:
            return redirect('myChild')
    elif request.session.has_key('age_range'):
        age_group = request.session['age_range']
    else:
        age_group = 0
    sub_headings = cache.get(str(heading_id) + "_" + str(age_group))
    if sub_headings is None:
        sub_headings = SubHeading.objects.filter(Q(headingId=heading) & Q(ageGroup__age_group=age_group))
        cache.set(str(heading_id) + "_" + str(age_group), sub_headings, 60*15)
    child_name = None
    child_age = None
    select_age = None
    if request.user.is_authenticated:
        child = Child.objects.filter(Q(username=request.user) & Q(activate=True))
        if child:
            child_name = child[0].childName
            child_age = get_age_string(child[0])
        else:
            return redirect('myChild')
    if request.session.has_key('age_range'):
        select_age = age_group_to_string(request.session['age_range'])
    return render(request, 'heading.html', {
        'heading':heading,
        'subHeadings':sub_headings,
        'childName':child_name,
        'childAge':child_age,
        'selectedAge':select_age,
    })


@login_required
@disclaimer_required
def my_child(request):
    """ page to manage your childrens account """
    error = None
    if request.method == 'POST':
        if 'add' in request.POST:
            child_form = AddChildForm(request.POST)
            if child_form.is_valid():
                child_name = child_form.cleaned_data['childName']
                dob = child_form.cleaned_data['dob']
                new_child = Child(username=request.user, childName=child_name, dob=dob, activate=False)
                new_child.save()
                try:
                    post_url = "http://" + get_current_site(request).domain + reverse(child_activate)
                    make_post_call(post_url, data={'id':new_child.id})
                except RequestsConnectionError:
                    pass
            else:
                error = "No child above the age of 5 can be added"

    child_form = AddChildForm()
    children = Child.objects.filter(username=request.user)
    children_all_info = []
    for child in children:
        children_all_info.append((child, get_age_string(child)))
    return render(request, 'my_child.html', {
        'children':children_all_info,
        'childForm':child_form,
        'error':error,
    })

@login_required
@disclaimer_required
def child_manage(request):
    """ page to manage your childrens account """
    error = None
    if request.method == 'POST':
        if 'edit' in request.POST:
            child_form = EditChildForm(request.POST)
            if child_form.is_valid():
                child_name = child_form.cleaned_data['childName']
                dob = child_form.cleaned_data['dob']
                child_id = child_form.cleaned_data['childID']
                child = Child.objects.get(id=child_id)
                child.childName = child_name
                child.dob = dob
                child.save()
            else:
                error = "No child above the age of 5 can be added"
    children = Child.objects.filter(username=request.user)
    children_all_info = []
    for child in children:
        children_all_info.append((child, get_age_string(child)))
    return render(request, 'child_manage.html', {
        'children':children_all_info,
        'error':error,
    })

@require_POST
@login_required
def child_activate(request):
    """ make a child as active for a user so the information is shown for the seleted child """
    child_id = int(request.POST['id'])
    child = Child.objects.filter(id=child_id).first()
    if child.username != request.user:
        return JsonResponse({'status':0})
    active_child = Child.objects.filter(Q(username=request.user) & Q(activate=True)).first()
    if active_child:
        active_child.activate = False
        active_child.save()
    child.activate = True
    child.save()
    return JsonResponse({'status':1})

@require_POST
@login_required
def child_delete(request):
    """ delete a child object from the model """
    child_id = int(request.POST['id'])
    child = Child.objects.filter(id=child_id).first()
    if child is None:
        return JsonResponse({'status':0})
    if child.username != request.user:
        return JsonResponse({'status':0})
    if child.activate:
        child.delete()
        new_child = Child.objects.filter(username=request.user).first()
        new_child.activate = True
        new_child.save()
    else:
        child.delete()
    return JsonResponse({'status':1})


def user_logout(request):
    """ logout a signed in user or exit a skipped user and redirect to the index page """
    if request.session.has_key('age_range'):
        del request.session['age_range']
    if request.session.has_key('disclaimer'):
        del request.session['disclaimer']
    logout(request)
    return redirect('index')

@disclaimer_required
@age_required
def location_map(request):
    """ show a map of the nearest hospitals """
    api_key = config('GOOGLE_API')
    return render(request, 'map.html', {
        'api_key':api_key,
    })

@disclaimer_required
@age_required
def search(request):
    """ allow user to serach for some information quickly """
    if request.method == 'POST':
        results = {}
        query = request.POST.get('search')
        age_group = 0
        if request.user.is_authenticated:
            age_group = get_age_group(request)
            if age_group == 10:
                age_group = 0
        elif request.session.has_key('age_range'):
            age_group = request.session['age_range']
        sub_headings = cache.get(query.replace(" ", "") + "_" + str(age_group))
        if sub_headings is None:
            sub_headings = SubHeading.objects.filter((Q(headingId__text__icontains=query) | Q(headingId__categoryName__description__icontains=query)|\
            Q(headingId__categoryName__categoryName__icontains=query) | Q(title__icontains=query) | Q(text__icontains=query))\
            & Q(ageGroup__age_group=age_group)).distinct()
            if sub_headings.count() > 0:
                cache.set(query.replace(" ", "") + "_" + str(age_group), sub_headings, 60*15)
        if sub_headings.count() > 0:
            results.update({'status':1})
            data = []
            for sub_heading in sub_headings:
                title = str(sub_heading.title)
                text = str(sub_heading.text)
                heading_id = str(sub_heading.headingId.headingId)
                sub_heading_id = str(sub_heading.subHeadingId)
                data_dictonary = {'title':title, 'text':text, 'heading_id':heading_id, 'sub_heading_id':sub_heading_id}
                data.append(data_dictonary)
            results.update({'data':data})
        else:
            results.update({'status':0})
        return JsonResponse(results, safe=False)
    search_form = SearchForm()
    return render(request, 'search.html', {
        'form':search_form,
    })

def get_age_group(request):
    """ from the age of a child, get the appropriate age group or return 10 if child doesnt exsist """
    child = Child.objects.filter(Q(username=request.user) & Q(activate=True)).first()
    if child is None:
        return 10
    child_age = child.dob
    age_of_child = ((date.today().year - child_age.year)*12) + (date.today().month - child_age.month)
    if age_of_child <= 1:
        age_group = 0
    elif age_of_child < 3:
        age_group = 1
    elif age_of_child < 6:
        age_group = 2
    elif age_of_child < 12:
        age_group = 3
    elif age_of_child < 24:
        age_group = 4
    elif age_of_child <= 60:
        age_group = 5
    else:
        age_group = 0
    return age_group

@login_required
@disclaimer_required
def diary(request):
    """ show all the children for a user so that they could view that childs diary logs """
    children = Child.objects.filter(username=request.user)
    return render(request, 'diary.html', {
        'children':children,
    })

@login_required
@disclaimer_required
def diary_logs(request, child_id):
    """ all the logs for a child """
    error = None
    if request.method == 'POST':
        if request.POST.get('check_id') != str(0):
            log = DiaryLog.objects.filter(diary_id=request.POST.get('check_id')).first()
            result_form = DiaryLogEditForm(request.POST, request.FILES, instance=log)
        else:
            result_form = DiaryLogEditForm(request.POST, request.FILES)

        if result_form.is_valid():
            result_form.save()
        else:
            error = "Diary entry not added/edited"

    child = Child.objects.filter(id=child_id).first()
    if child.username != request.user:
        return redirect('index')
    logs = DiaryLog.objects.filter(child=child)
    form = DiaryLogEditForm(initial={'child':child, 'check_id':0})
    edit_logs = []
    for log in logs:
        edit_logs.append(DiaryLogEditForm(instance=log, initial={'check_id':log.diary_id}))
    return render(request, 'diary_logs.html', {
        'child':child,
        'logs':logs,
        'form':form,
        'edit_logs':edit_logs,
        'error':error,
    })

@require_POST
@login_required
def diary_delete(request):
    """ delete a diary log object from the model """
    diary_id = int(request.POST['id'])
    diary_entry = DiaryLog.objects.filter(diary_id=diary_id).first()
    if diary_entry is None:
        return JsonResponse({'status':0})
    if diary_entry.child.username != request.user:
        return JsonResponse({'status':0})
    diary_entry.delete()
    return JsonResponse({'status':1})
