# here we write the views file
# importing the neccessary packages and modules

# create a guest user first to work properly, it should have the id as 1
import csv
import os
from unicodedata import name
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from math import fabs
import random
from PIL import Image
from django.http import HttpResponse, JsonResponse, FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.shortcuts import redirect, render
from twilio.rest import Client
# from Aldshop.settings import TWILIO_AUTH_TOKEN, TWILIO_SSID
from Aldshop.forms import add_category, add_product_form, upload_product_image
from Aldshop.models import Banners, Cart, Category, Coupon, Coupon_history, Orders, Products, References, \
    Return_request, Users, Address, Wallet_history
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import datetime
from datetime import date, timedelta

# end of importing files

# end

# declaring or initializing the global variables
global upload_status
upload_status = 0
current_date = datetime.date.today()
duration = 'Today'
otp = '0'
delivery_charge = 10
orders = ''
image_1 = ''
image_2 = ''
image_3 = ''
image_4 = ''
cart_count = 0
navigation = ''


# end

# Create your views here.

# ________starting the functions to handle our app backend__________
@never_cache
def root(request):
    '''Redirecting to the home page'''
    data = request.GET.keys()
    print('data', data)
    return redirect('/user_home')


# __________admin side___________

@never_cache
@never_cache
def admin_sign_in(request):
    if 'admin' in request.session:
        if request.session['admin'] == False:
            return redirect('/admin_sign_in')
        else:
            admin_email = request.session['admin']

    if request.method == 'POST':
        # collecting the data from the ajax request in user_sign_in.html
        user_email = request.POST.get('user_email')
        user_password = request.POST.get('user_password')

        # getting all the available users
        users = Users.objects.all()

        if len(users) > 0:
            for user in users:
                if user_email == user.email:
                    if user_password == user.password:
                        user = Users.objects.get(email=user_email)
                        if user.active_status == 'active':
                            if user.is_admin == 'true':
                                request.session['admin'] = user_email
                                user_authentication_status = 'success'
                                break
                            user_authentication_status = 'user_not_admin'
                            break
                        user_authentication_status = 'admin_not_active'
                        break
                    user_authentication_status = 'wrong_password'
                    break
                user_authentication_status = 'admin_not_found'
            return JsonResponse({'user_authentication_status': user_authentication_status})
        else:
            return JsonResponse({'user_authentication_status': 'admin_not_found'})
    return render(request, 'admin_sign_in.html')


##########################################################################################################################
@never_cache
def admin_sign_out(request):
    '''handle the admin signin request'''
    del request.session['admin']
    return render(request, 'admin_sign_in.html')


#########################################################################################################################

@never_cache
def admin_panel(request):
    global upload_status
    upload_status = 0
    admin = ''
    if 'admin' in request.session:
        if request.session['admin'] == False:
            return redirect('/admin_sign_in')
        else:
            admin_email = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin_email)
    user_count = Users.objects.all().count()
    sales = Orders.objects.filter(status='Delivered')
    revenue = 0
    for sale in sales:
        revenue = revenue + sale.total_price
    return render(request, 'admin_panel.html',
                  {'admin': this_admin, 'duration': '', 'sales': sales.count, 'customer_count': user_count,
                   'revenue': revenue})


#########################################################################################################################

@never_cache
def admin_add_product(request):
    admin = ''
    global upload_status
    # checking the status of the admin
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    # handles the post request
    if request.method == 'POST':
        global image_1, image_2, image_3, image_4, form
        if upload_status == 1:
            upload_status = 2
            form = request.FILES.get('image_1')
            x = float(request.POST.get('x'))
            print(x)
            y = float(request.POST.get('y'))
            print(y)
            h = float(request.POST.get('height'))
            print(h)
            w = float(request.POST.get('width'))
            print(w)
            new_product = Products.objects.last()
            product = Products.objects.get(id=new_product.id)
            product.image_1 = form
            product.save()
            print(x, y, w, h)
            image = Image.open(product.image_1)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            image = resized_image.save('media/{}'.format(product.image_1))
            print(product.image_1)
            print('received_image_1')
            # return redirect('/admin_add_product')
        elif upload_status == 2:
            upload_status = 3
            form = request.FILES.get('image_2')
            print(form)
            x = float(request.POST.get('x'))
            print(x)
            y = float(request.POST.get('y'))
            print(y)
            h = float(request.POST.get('height'))
            print(h)
            w = float(request.POST.get('width'))
            print(w)
            new_product = Products.objects.last()
            product = Products.objects.get(id=new_product.id)
            product.image_2 = form
            product.save()
            print(x, y, w, h)
            image = Image.open(product.image_2)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            image = resized_image.save('media/{}'.format(product.image_2))
            print(product.image_2)
            # return redirect('/admin_add_product')
        elif upload_status == 3:
            upload_status = 4
            form = request.FILES.get('image_3')
            print(form)
            x = float(request.POST.get('x'))
            print(x)
            y = float(request.POST.get('y'))
            print(y)
            h = float(request.POST.get('height'))
            print(h)
            w = float(request.POST.get('width'))
            print(w)
            new_product = Products.objects.last()
            product = Products.objects.get(id=new_product.id)
            product.image_3 = form
            product.save()
            print(x, y, w, h)
            image = Image.open(product.image_3)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            image = resized_image.save('media/{}'.format(product.image_3))
            print(product.image_3)
            # return redirect('/admin_add_product')
        elif upload_status == 4:
            upload_status = 0
            form = request.FILES.get('image_4')
            print(form)
            x = float(request.POST.get('x'))
            print(x)
            y = float(request.POST.get('y'))
            print(y)
            h = float(request.POST.get('height'))
            print(h)
            w = float(request.POST.get('width'))
            print(w)
            new_product = Products.objects.last()
            product = Products.objects.get(id=new_product.id)
            product.image_4 = form
            product.save()
            print(x, y, w, h)
            image = Image.open(product.image_4)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            image = resized_image.save('media/{}'.format(product.image_4))
            print(product.image_4)
            return redirect(admin_thankyou_for_adding_product)
            # return redirect('/admin_add_product')
        elif upload_status == 0:
            upload_status = 1
            # checking whether all the input fields are filled,not empty and are filled with proper inputs
            # getting datas from the specific fields from the frontend
            form = add_product_form(request.POST, request.FILES)
            category = request.POST.get('category')
            specification = request.POST.get('specification')
            # print(category)
            # print(category)
            print('validating...')
            if form.is_valid():
                form.save(commit=False)
                form.category = category
                form.specification = specification
                form.save()
            #     return redirect('/admin_add_product')
            # return HttpResponse('failed')
            # trying to creating new product
    if upload_status == 0:
        form = add_product_form()
        form_categories = Category.objects.all()
        return render(request, 'admin_add_product.html',
                      {'form': form, 'form_categories': form_categories, 'admin': this_admin})
    elif upload_status == 1:
        form = add_product_form()
        return render(request, 'upload_image.html', {'index': 1, 'form': form})
    elif upload_status == 2:
        form = add_product_form()
        return render(request, 'upload_image.html', {'index': 2, 'form': form})
    elif upload_status == 3:
        form = add_product_form()
        return render(request, 'upload_image.html', {'index': 3, 'form': form})
    elif upload_status == 4:
        form = add_product_form()
        return render(request, 'upload_image.html', {'index': 4, 'form': form})


#########################################################################################################################

def admin_thankyou_for_adding_product(request):
    return render(request, 'admin_thankyou_for_adding_product.html')


#########################################################################################################################

@never_cache
def admin_list_product(request):
    admin = ''
    ppp = 4
    current_page = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    products = Products.objects.all()
    if request.method == 'POST':
        current_page = request.POST.get('page_number')
    p = Paginator(products, ppp)
    page_obj = p.get_page(current_page)
    available_pages = []
    pages = int(products.count() / ppp)
    for i in range(0, pages):
        available_pages.append(i)
    context = {
        'admin': admin,
        'products': page_obj,
        'admin': this_admin,
        'available_pages': available_pages,
        'current_page': current_page
    }
    return render(request, 'admin_list_product.html', context)


#########################################################################################################################
@never_cache
def admin_add_category(request):
    admin = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    if request.method == 'POST':
        # getting datas from the specific fields from the frontend
        form = add_category(request.POST, request.FILES)
        # checking whether all the input fields are filled,not empty and are filled with proper inputs
        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                category_id = Category.objects.get(name=str(name))
                if category_id is not None:
                    print('category already exist')
                    return render(request, 'admin_add_category.html',
                                  {'form': form, 'message': 'category already exist', 'admin': this_admin})
            except:
                # adding new details to the company_info table/model
                # form.cleaned_data['name'] = category_id
                form.save()
                return render(request, 'admin_add_category_success.html')
        return HttpResponse('failed')
        # handling get request
        # trying to creating new product
    form = add_category()
    return render(request, 'admin_add_category.html', {'form': form})


#########################################################################################################################
# @never_cache
def admin_edit_Product(request):
    admin = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    products = Products.objects.all()
    if request.method == 'POST':
        global current_product
        id = request.POST.get('product_id')
        print(id)
        product = Products.objects.get(id=id)
        product.name = request.POST.get('product_name')
        product.price = request.POST.get('product_price')
        product.category = request.POST.get('product_category')
        product.description = request.POST.get('product_description')
        product.specification = request.POST.get('product_specification')
        product.stock_available = request.POST.get('product_stock_available')
        product.available_status = request.POST.get('product_status')

        if request.FILES.get('image_1') == None:
            product.image_1 = product.image_1
            print('product image 1 not found')
        else:
            try:
                os.remove(product.image_1.path)
            except:
                pass
            product.image_1 = request.FILES.get('image_1')

        if request.FILES.get('image_2') == None:
            product.image_2 = product.image_2
            print('product image 2 not found')
        else:
            try:
                os.remove(product.image_2.path)
            except:
                pass
            product.image_2 = request.FILES.get('image_2')
        if request.FILES.get('image_3') == None:
            product.image_3 = product.image_3
            print('product image 3 not found')
        else:
            try:
                os.remove(product.image_3.path)
            except:
                pass
            product.image_3 = request.FILES.get('image_3')
        if request.FILES.get('image_4') == None:
            product.image_4 = product.image_4
            print('product image 4 not found')
        else:
            try:
                os.remove(product.image_4.path)
            except:
                pass
            product.image_4 = request.FILES.get('image_4')
        product.save()
        return render(request, 'admin_edit_product_success.html')

    action = request.GET.get('action')
    product_id = request.GET.get('product_id')
    print(action)
    print(product_id)
    product = Products.objects.get(id=product_id)
    categories = Category.objects.all()

    if action == 'edit':
        return render(request, 'admin_edit_product.html',
                      {'product': product, 'admin': this_admin, 'categories': categories})
    elif action == 'delete':
        try:
            os.remove(product.image_1.path)
            os.remove(product.image_2.path)
            os.remove(product.image_3.path)
            os.remove(product.image_4.path)
        except:
            pass
        product.delete()
        return redirect(admin_list_product)
    return redirect('/admin_panel')


#########################################################################################################################

@never_cache
def admin_list_category(request):
    admin = ''
    ppp = 3
    current_page = 1
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    categories = Category.objects.all()
    if request.method == 'POST':
        current_page = request.POST.get('page_number')
    p = Paginator(categories, ppp)
    page_obj = p.get_page(current_page)
    available_pages = []
    pages = int(categories.count() / ppp)
    for i in range(0, pages):
        available_pages.append(i)
    return render(request, 'admin_list_category.html',
                  {'admin': admin, 'categories': page_obj, 'admin': this_admin, 'available_pages': available_pages,
                   'current_page': current_page})


#########################################################################################################################
@never_cache
def admin_edit_category(request, cat_id):
    admin = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    category = Category.objects.get(id=cat_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if image is None:
            category.image = Category.objects.get(id=cat_id).image
        else:
            try:
                os.remove(category.image.path)
            except:
                pass
            category.image = image
        category.name = name
        category.save()
        return redirect(admin_list_category)
    return render(request, 'admin_edit_category.html', {'category': category, 'admin': this_admin})


#########################################################################################################################
@never_cache
def admin_category_delete(request):
    '''handles the category delete request '''
    admin = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    try:
        os.remove(Category.objects.get(
            id=request.POST.get('category_id')).image.path)
    except:
        pass
    Category.objects.get(
        id=request.POST.get('category_id')).delete()
    return JsonResponse({'status': 'done'})


#########################################################################################################################

@never_cache
def admin_list_customer(request):
    admin = ''
    current_page = 1
    ppp = 5
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    try:
        users = Users.objects.all()
    except:
        users = ''
        pass
    if request.method == 'POST':
        current_page = request.POST.get('page_number')
    p = Paginator(users, ppp)
    page_obj = p.get_page(current_page)
    available_pages = []
    pages = int(users.count() / ppp)
    for i in range(0, pages):
        available_pages.append(i)
    return render(request, 'admin_list_customer.html',
                  {'users': page_obj, 'admin': this_admin, 'available_pages': available_pages,
                   'current_page': current_page})


#########################################################################################################################
@never_cache
def admin_update_user_status(request):
    admin = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    if request.method == 'POST':
        status = request.POST.get('status')
        email = request.POST.get('email')
        # print(status)
        if status == 'true':
            status = 'block'
        else:
            status = 'active'
        # print(email)
        #     getting the user details for update
        customer = Users.objects.get(email=email)
        customer.active_status = status
        customer.save()
        print(customer.email)
        print(customer.active_status)
        return JsonResponse({'status': status})
    customers = Users.objects.all()
    return render(request, 'edit_customer.html', {'users': customers, 'admin': this_admin})


#########################################################################################################################

@never_cache
def admin_order_details(request, order_id):
    admin = ''
    address = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    order = Orders.objects.get(id=order_id)
    try:
        address = Address.objects.get(id=order.Address)
    except:
        pass
    if order.status == 'ordered':
        next_status = 'shipped'
    elif order.status == 'shipped':
        next_status = 'Out For Delivery'
    elif order.status == 'Out For Delivery':
        next_status = 'delivered'
    elif order.status == 'return requested':
        next_status = 'Returned'
    elif order.status == 'Returned':
        next_status = 'Refunded'
    else:
        next_status = 'Pending'
    return render(request, 'admin_order_details.html',
                  {'order': order, 'address': address, 'next_status': next_status, 'admin': this_admin})


#########################################################################################################################

@never_cache
def admin_change_order_status(request):
    order_status = request.POST.get('status')
    order_id = request.POST.get('order_id')
    print(order_id)
    change_order_status = Orders.objects.get(id=order_id)
    change_order_status.status = order_status
    change_order_status.save()
    return JsonResponse({'status': 'success'})


#########################################################################################################################

@never_cache
def admin_update_order_status(request):
    '''handles the user update order status request from the user'''
    global navigation
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_status = request.POST.get('order_status')
        product = Orders.objects.get(id=order_id)
        navigation = '#' + str(request.POST.get('navigate'))
        print(product.status)
        product.status = 'canceled'
        product.save()
    return JsonResponse({'status': 'canceled'})


#########################################################################################################################

@never_cache
def admin_list_orders(request):
    admin = ''
    ppp = 10
    current_page = 1
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)

    orders = Orders.objects.all()
    if request.method == 'POST':
        current_page = request.POST.get('page_number')
    p = Paginator(orders, ppp)
    page_obj = p.get_page(current_page)
    available_pages = []
    pages = int(orders.count() / ppp)
    for i in range(0, pages):
        available_pages.append(i)
    return render(request, 'admin_list_orders.html',
                  {'admin': this_admin, 'orders': page_obj, 'available_pages': available_pages,
                   'current_page': current_page})


#########################################################################################################################

@never_cache
def admin_edit_banner(request):
    admin = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    try:
        banner1 = Banners.objects.get(id=1)
        banner2 = Banners.objects.get(id=2)
        banner3 = Banners.objects.get(id=3)
    except:
        return render(request, 'admin_add_banner.html')
    if request.method == 'POST':
        if request.POST.get('banner') == '1':
            banner_1_image = request.FILES.get('banner_1_image')
            banner_1_heading = request.POST.get('banner_1_heading')
            banner_1_description = request.POST.get('banner_1_description')
            banner_1 = Banners.objects.get(id=1)
            banner_1.heading = banner_1_heading
            banner_1.description = banner_1_description
            if banner_1_image != None:
                os.remove(banner_1.image.path)
                banner_1.image = banner_1_image
            banner_1.save()
            return redirect(admin_edit_banner)
        if request.POST.get('banner') == '2':
            banner_2_image = request.FILES.get('banner_2_image')
            banner_2_heading = request.POST.get('banner_2_heading')
            banner_2_description = request.POST.get('banner_2_description')
            banner_2 = Banners.objects.get(id=2)
            banner_2.heading = banner_2_heading
            banner_2.description = banner_2_description
            if banner_2_image != None:
                os.remove(banner_2.image.path)
                banner_2.image = banner_2_image
            banner_2.save()
            return redirect(admin_edit_banner)
        if request.POST.get('banner') == '3':
            banner_3_image = request.FILES.get('banner_3_image')
            banner_3_heading = request.POST.get('banner_3_heading')
            banner_3_description = request.POST.get('banner_3_description')
            banner_3 = Banners.objects.get(id=3)
            banner_3.heading = banner_3_heading
            banner_3.description = banner_3_description
            if banner_3_image != None:
                os.remove(banner_3.image.path)
                banner_3.image = banner_3_image
            banner_3.save()
            return redirect(admin_edit_banner)
    return render(request, 'admin_edit_banner.html',
                  {'banner1': banner1, 'banner2': banner2, 'banner3': banner3, 'admin': this_admin})


#########################################################################################################################

@never_cache
def admin_add_banner(request):
    if request.method == 'POST':
        # banner 1 details
        banner_1_heading = request.POST.get('banner_1_heading')
        banner_1_description = request.POST.get('banner_1_description')
        banner_1_image = request.FILES.get('banner_1_image')
        # banner 2 details
        banner_2_heading = request.POST.get('banner_2_heading')
        banner_2_description = request.POST.get('banner_2_description')
        banner_2_image = request.FILES.get('banner_2_image')
        # banner 3 details
        banner_3_heading = request.POST.get('banner_3_heading')
        banner_3_description = request.POST.get('banner_3_description')
        banner_3_image = request.FILES.get('banner_3_image')
        print(banner_1_heading, banner_1_description, banner_2_heading, banner_2_description, banner_3_heading,
              banner_3_description)
        banner1_add = Banners.objects.create(heading=banner_1_heading, description=banner_1_description,
                                             image=banner_1_image)
        banner2_add = Banners.objects.create(heading=banner_2_heading, description=banner_2_description,
                                             image=banner_2_image)
        banner3_add = Banners.objects.create(heading=banner_3_heading, description=banner_3_description,
                                             image=banner_3_image)
        banner1_add.save()
        banner2_add.save()
        banner3_add.save()
        return redirect(admin_edit_banner)
    return HttpResponse('banner failed to add')


#########################################################################################################################


# _____________users_views________________    
def user_base(request):
    return render(request, 'user_base.html')


#########################################################################################################################

@never_cache
def user_home(request):
    global cart_count
    '''Render and control the datas in the user home page'''
    user = ''
    try:
        if 'user' in request.session:
            user_email = request.session['user']
            user = Users.objects.get(email=user_email)
            cart_count = Cart.objects.filter(user=user).count()
        else:
            user = 'guest'
            guest_id = request.COOKIES['sessionid']
            cart_count = Cart.objects.filter(guest_id=guest_id).count()
    except:
        pass
    try:
        banner1 = Banners.objects.get(id=1)  # getting the banner data
        banner2 = Banners.objects.get(id=2)  # getting the banner data
        banner3 = Banners.objects.get(id=3)  # getting the banner data
    except:
        banner1 = ''  # assigning null to the banners if there is an issue in getting the banner
        banner2 = ''  # assigning null to the banners if there is an issue in getting the banner
        banner3 = ''  # assigning null to the banners if there is an issue in getting the banner
    try:
        products = Products.objects.all()
        trusted_products = Products.objects.filter(is_trusted='trusted')
        best_offer_products = Products.objects.all()
        rated_products = Products.objects.filter(rating=5)
    except:
        products = ''
    try:
        categories = Category.objects.all()
    except:
        categories = ''
    print(products)
    context = {
        'user': user,
        'banner1': banner1,
        'banner2': banner2,
        'banner3': banner3,
        'products': products,
        'categories': categories,
        'trusted_products': trusted_products,
        'best_offer_products': best_offer_products,
        'rated_products': rated_products,
        'cart_count': cart_count,
    }
    return render(request, 'user_home.html', context)


#############################################################################################################################
@never_cache
def user_sign_up(request):
    '''handles the user signup request from the user'''
    if request.method == 'POST':
        # collecting the data from the ajax request in user_sign_in.html
        user_full_name = request.POST.get('user_full_name')
        user_email = request.POST.get('user_email')
        user_password = request.POST.get('user_password')
        user_contact_number = request.POST.get('user_contact_number')
        profile_image = request.FILES.get('profile_image')
        all_users = Users.objects.all()
        for user in all_users:
            if user_email == user.email:
                return render(request, 'user_sign_up.html', {'message': 'The user Already have an Account.'})
        for user in all_users:
            if user_contact_number == user.contact_number:
                return render(request, 'user_sign_up.html', {'message': 'The Phone Number Already Exist!'})
        referece_id = random.randrange(1000000000, 9999999999)
        # getting all the available users
        try:
            new_user = Users.objects.create(
                full_name=user_full_name,
                email=user_email,
                password=user_password,
                contact_number=user_contact_number,
                profile_image=profile_image,
                reference_id=referece_id
            )
            new_user.save()
            user_sign_up_status = 'user_created'
            return redirect(welcome_new_user)
        except:
            user_sign_up_status = 'failed'
        return redirect(user_home)
    return render(request, 'user_sign_up.html')


# end
###############################################################################################


@never_cache
def user_sign_in(request):
    '''handle the sign in request from the user'''

    def configuring_cart(email):
        print('checking the cart of guest user on this system...')
        guest_id = request.COOKIES['sessionid']
        user = Users.objects.get(email=email)
        # cart_items = Cart.objects.filter(user=user)
        guest_cart_items = Cart.objects.filter(guest_id=guest_id)
        print('copying the cart products to the user cart if any products exists...')
        count = 0
        for product in guest_cart_items:
            product.user = user
            product.save()
            count += 1
            print('copied {} product'.format(count))

        pass

    if 'user' in request.session:
        return redirect(user_home)
    if request.method == 'POST':

        # collecting the data from the ajax request in user_sign_in.html
        user_email = request.POST.get('user_email')
        user_password = request.POST.get('user_password')
        print('got the user input data')
        # getting all the available users
        users = Users.objects.all()
        if len(users) > 0:
            for user in users:
                if user_email == user.email:
                    if user_password == user.password:
                        if user.active_status == 'active':
                            request.session['user'] = user_email
                            user_authentication_status = 'success'
                            configuring_cart(user_email)
                            break
                        user_authentication_status = 'user_not_active'
                        break
                    user_authentication_status = 'wrong_password'
                    break
                user_authentication_status = 'user_not_found'
            return JsonResponse({'user_authentication_status': user_authentication_status})
        else:
            return JsonResponse({'user_authentication_status': 'user_not_found'})
    return render(request, 'user_sign_in.html')


# end
###############################################################################################

def welcome_new_user(request):
    return render(request, 'welcome_new_user.html')


@never_cache
def user_sign_out(request):
    '''handle the user signout page'''
    del request.session['user']
    return redirect('/user_home')


# end

@never_cache
def search_engine(request):
    '''handles the product search requests'''
    keyword = request.GET.get('keyword')
    available_product = Products.objects.all()
    result = []
    for product in available_product:
        keyword = str(str(keyword).upper())
        all_products = str(str(product.name).upper())
        if keyword in all_products:
            print('found in product')
            search_result = Products.objects.get(id=product.id)
            result.append(search_result)
    context = {
        'search_results': result,
        'cart_count': cart_count,
    }
    return render(request, 'user_search_results.html', context)


#########################################################################################################################

@never_cache
def user_product_detail(request, product_id):
    '''Render and control the data in the user product detail page'''
    global cart_count
    user = ''
    if 'user' in request.session:
        user = request.session['user']
        this_user = Users.objects.get(email=user)
    else:
        user = 'guest'
        this_user = 'guest'
    product = Products.objects.get(id=product_id)
    category = Products.objects.filter(category=product.category)
    categories = Category.objects.all()
    context = {
        'product': product,
        'category': category,
        'user': this_user,
        'categories': categories,
        'cart_count': cart_count
    }
    return render(request, 'user_product_detail.html', context)


#########################################################################################################################

@never_cache
def user_add_to_cart(request):
    '''working while the user cliick add to cart'''
    print('trying to add product to the cart')
    response = 'failed'
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product = Products.objects.get(id=product_id)
        product_offer = product.offer_percentage
        discount = int(product.price) * (int(product_offer) / 100)
        total_price = product.price - discount
        if 'user' in request.session:
            user = request.session['user']
            user = Users.objects.get(email=user)
            cart_products = Cart.objects.filter(user=user)
            print('offer applied ', total_price)

            status = 0
            for product in cart_products:
                print(product_id, product.product.id)
                if str(product.product.id) == str(product_id):
                    print('product is updating')
                    product.quantity += 1
                    product.save()
                    status = 1
                    response = 'product_added'
                    break

            if status == 0:
                print('new to cart')
                new_cart_product = Cart.objects.create(
                    product_id=product_id,
                    user_id=user.id,
                    quantity=1,
                    total_price=int(total_price),
                )
                new_cart_product.save()
                response = 'product_added'

            return JsonResponse({'response': response})

        else:
            guest_id = request.COOKIES['sessionid']
            print('user is not found. trying to get a guest user account...')
            print('your guest user acoount id is ', guest_id)
            cart_products = Cart.objects.filter(guest_id=guest_id)

            status = 0
            for product in cart_products:
                print(product_id, product.product.id)
                if str(product.product.id) == str(product_id):
                    print('product is updating')
                    product.quantity += 1
                    product.save()
                    status = 1
                    response = 'product_added'
                    break

            if status == 0:
                print('new to cart')
                new_cart_product = Cart.objects.create(
                    product_id=product_id,
                    guest_id=guest_id,
                    user_id=1,
                    quantity=1,
                    total_price=int(total_price),
                )
                new_cart_product.save()
                response = 'product_added'

            return JsonResponse({'response': response})

    return JsonResponse({'response': response})


#########################################################################################################################

@never_cache
def user_check_cart_or_shop(request):
    '''used to show that the cart is empty'''
    return render(request, 'user_check_cart_or_shop.html')


#########################################################################################################################

@never_cache
def user_delete_cart_item(request):
    if request.method == 'POST':
        cart_id = request.POST.get('id')
        delete_product = Cart.objects.get(id=cart_id).delete()
        print('one item from the cart is deleted')
        return JsonResponse({'deleted': 'deleted'})


#########################################################################################################################

@never_cache
def user_view_cart(request):
    '''Render view cart in user side'''
    global cart_count
    sub_total = 0
    # trying to add the order to the cart
    try:
        if 'user' in request.session:
            user = request.session['user']
            user = Users.objects.get(email=user)
            products = Cart.objects.filter(user=user.id)
        else:
            user = 'guest'
            guest_id = request.COOKIES['sessionid']
            products = Cart.objects.filter(guest_id=guest_id)
    except:
        user = ''
        products = ''

    if len(products) == 0:
        return render(request, 'user_cart_empty.html')
    product_offer = 0
    for price in products:
        # price.total_price = Products.objects.get(id = price.product.id).price
        print('product with discount', price.total_price)
        sub_total = int(sub_total) + int(price.total_price)
    # total = sub_total+delivery_charge
    special_offer = product_offer
    request.session['sub_total'] = sub_total
    request.session['checkout_status'] = 'True'
    context = {
        'user': user,
        'products': products,
        'sub_total': sub_total,
        'special_offer': special_offer,
        'delivery_charge': delivery_charge,
        'cart_count': cart_count
    }
    response = render(request, 'user_cart_view.html', context)

    return response


# end
#############################################################################################################################


@never_cache
def user_checkout(request):
    '''handles the checkout page'''
    global cart_count
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    sub_total = request.session['sub_total']
    address = Address.objects.filter(email=user)
    user = Users.objects.get(email=user)
    context = {
        'sub_total': sub_total,
        'address': address,
        'user': user,
        'default_address_id': 1,
        'total_razorpay': sub_total * 100,
        'cart_count': cart_count
    }
    return render(request, 'user_checkout.html', context)


#############################################################################################################################

def user_add_address(request):
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    if request.method == 'POST':
        this_user = Users.objects.get(email=user)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        building_name = request.POST.get('building_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')
        alt_contact = request.POST.get('alt_contact')
        user_new_address = Address.objects.create(
            email=user,
            first_name=first_name,
            last_name=last_name,
            building_name=building_name,
            street=street,
            city=city,
            state=state,
            pincode=pincode,
            contact=contact,
            alt_contact=alt_contact,
        )
        user_new_address.save()
        print('new address of the user  is saved')
        return redirect('/user_checkout')
    return render(request, 'user_add_address.html')


#########################################################################################################################

@never_cache
def user_otp_sign_in(request):
    '''handle the user otp sign in'''
    otp_sign_in_user_status = ''
    if request.method == 'POST':
        print('helloooo')
        contact_number = request.POST.get('user_num')
        request.session['user_num'] = contact_number
        print(contact_number)

        if Users.objects.filter(contact_number=contact_number).exists():
            print('heloooo')

            user = Users.objects.get(contact_number=contact_number).email
           # client = Client('ACe76401d83965afd3d5d67ecb05038e1f',
            #                'f5ba986fbd2c054c446f74dd299fde5b')
            verification = client.verify \
                .v2 \
             #   .services('VA45231356f6ed0671efb52f636ae50624') \
                .verifications \
                .create(to='+91{}'.format(contact_number), channel='sms')
            request.session['user'] = user
            user_authentication_status = 'success'
            otp_sign_in_user_status = 'success'
            return JsonResponse({'otp_sign_in_user_status': otp_sign_in_user_status})
        else:
            return render(request, 'user_otp_sign_in.html', {'message': "invalid phone number"})
    else:
        return render(request, 'user_otp_sign_in.html')


#########################################################################################################################        

@never_cache
def user_otp_sign_in_validation(request):
    '''handle the user otp validation'''
    if request.method == 'POST':
        otp_1 = request.POST.get('otp_1')
        otp_2 = request.POST.get('otp_2')
        otp_3 = request.POST.get('otp_3')
        otp_4 = request.POST.get('otp_4')
        # var err = document.getElementById('err')

        user_otp = str(otp_1 + otp_2 + otp_3 + otp_4)
        print(otp)
        print(user_otp)
        contact_number = request.session['user_num']
        #client = Client('ACe76401d83965afd3d5d67ecb05038e1f',
         #               'f5ba986fbd2c054c446f74dd299fde5b')
        verification_check = client.verify \
            .v2 \
           # .services('VA45231356f6ed0671efb52f636ae50624') \
            .verification_checks \
            .create(to='+91{}'.format(contact_number), code=user_otp)

        print(verification_check.status)
        user_authentication_status = 'approved'
        # user_authentication_status = 'wrong_otp'
        # if str(user_otp) == str(otp):
        #     user_authentication_status = 'otp_verified'
        #     user = Users.objects.get(contact_number = str(request.session['contact_number']))
        #     request.session['user'] = user.email
        return JsonResponse({'user_authentication_status': user_authentication_status})
    return render(request, 'user_otp_sign_in_validation.html')


#########################################################################################################################

@never_cache
def user_account(request):
    '''handle the user account'''
    global navigation
    global cart_count
    refered_people = ''
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    this_user = Users.objects.get(email=user)
    orders = Orders.objects.filter(user_id=this_user.id).order_by('-id')
    address = Address.objects.filter(email=this_user.email)
    refered_people_details = References.objects.filter(user_id=this_user.id)
    delivered_orders = Orders.objects.filter(
        user_id=this_user.id, status='delivered')
    for order in delivered_orders:
        if int(current_date.day) >= int(order.Order_day) + 7:
            order.status = 'delivered_no_return'
            order.save()
    for order in orders:
        if order.status == 'Refunded':
            order.status = 'completed'
            this_user.wallet_balance = int(this_user.wallet_balance) + int(order.total_price)
            this_user.save()
            order.save()
            add_to_wallet_history(order)  # passing order instance
    for order in orders:
        if order.status == 'canceled':
            if order.payment_method != 'cod':
                order.status = 'completed'
                this_user.wallet_balance = int(this_user.wallet_balance) + int(order.total_price)
                this_user.save()
                order.save()
                add_to_wallet_history(order)
    print(refered_people_details)
    peoples = []
    for people in refered_people_details:
        print(people.refered_user_id)
        user = Users.objects.get(id=(people.refered_user_id))
        peoples.append(user.full_name)
    context = {
        'user': this_user,
        'orders': orders,
        'address': address,
        'refered_people_details': peoples,
        'cart_count': cart_count,
        'navigation': navigation
    }

    return render(request, 'user_account.html', context)


#########################################################################################################################
@never_cache
def user_update_cart(request):
    '''this will handle the quartity updations in cart'''
    user = 'guest'
    if 'user' in request.session:
        user = request.session['user']
    else:
        guest_id = request.COOKIES['sessionid']

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart_id = request.POST.get('cart_id')
        task = request.POST.get('task')
        print(task)
        try:
            user = Users.objects.get(email=user)
        except:
            user = guest_id

        product = Cart.objects.get(id=cart_id)
        stock = Products.objects.get(id=product.product.id)
        discount = int(stock.price) * (int(stock.offer_percentage) / 100)
        orginal_price_with_discount = stock.price - discount
        stock_balance = stock.stock_available
        print('got quantity', quantity)
        if task == 'plus':
            updated_quantity = int(quantity) + 1
            if stock_balance > 1:
                product.quantity = updated_quantity
                print('updated quantity', updated_quantity)
                # stock manage
                stock.stock_available = stock.stock_available - 1
            else:
                updated_quantity = quantity
        else:
            updated_quantity = int(quantity) - 1
            if updated_quantity >= 1:
                product.quantity = updated_quantity
                print('updated quantity', updated_quantity)
                # stock manage
                stock.stock_available = stock.stock_available + 1
            else:
                updated_quantity = quantity
        print('orginal_price_with_discount', orginal_price_with_discount)
        total_prize = int(int(orginal_price_with_discount)
                          * int(updated_quantity))
        product.total_price = int(total_prize)
        stock.save()
        print('stock balance ', stock.stock_available)
        product.save()
        try:
            all_cart_products = Cart.objects.filter(user=user.id)
        except:
            all_cart_products = Cart.objects.filter(guest_id=guest_id)

        sub_total = 0
        for product in all_cart_products:
            sub_total = int(sub_total) + int(product.total_price)
        # print(sub_total)
        request.session['sub_total'] = sub_total
        print('saved the changes in database')
        return JsonResponse({
            'updated_quantity': updated_quantity,
            'stock_available': stock.stock_available,
            'total_price': product.total_price,
            'sub_total': int(sub_total),
            'delivery_charge': delivery_charge,
        })
    return JsonResponse({'user': 'user_info'})


# end
#############################################################################################################################


@never_cache
def user_update_user(request, user_id):
    '''used to update the user information'''
    user_full_name = request.POST.get('user_full_name')
    user_contact_number = request.POST.get('user_contact_number')
    profile_image = request.FILES.get('profile_image')
    print(user_full_name)
    print(user_contact_number)
    user = Users.objects.get(id=user_id)
    user.full_name = user_full_name
    user.contact_number = user_contact_number
    if profile_image != None:
        try:
            os.remove(user.profile_image.path)
        except:
            pass
        user.profile_image = profile_image
    user.save()
    return redirect(user_account)


#########################################################################################################################

@never_cache
def user_update_order_status(request):
    '''handles the user update order status request from the user'''
    global navigation
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_status = request.POST.get('order_status')
        product = Orders.objects.get(id=order_id)
        navigation = '#' + str(request.POST.get('navigate'))
        print(product.status)
        product.status = 'canceled'
        product.save()
    return JsonResponse({'status': 'canceled'})


#########################################################################################################################

@never_cache
def user_edit_address(request, address_id):
    '''handle user edit address data'''
    address_prefill = Address.objects.get(id=address_id)
    if request.method == 'POST':
        address_prefill.first_name = request.POST.get('first_name')
        address_prefill.last_name = request.POST.get('last_name')
        address_prefill.building_name = request.POST.get('building_name')
        address_prefill.street = request.POST.get('street')
        address_prefill.city = request.POST.get('city')
        address_prefill.state = request.POST.get('state')
        address_prefill.pincode = request.POST.get('pincode')
        address_prefill.contact = request.POST.get('contact')
        address_prefill.alt_contact = request.POST.get('alt_contact')
        address_prefill.save()
        print('address has been updated')
        return redirect('/user_account')
    return render(request, 'user_edit_address.html', {'address_prefill': address_prefill})


#########################################################################################################################


@never_cache
def user_delete_address(request):
    '''handle the delete address'''
    address_id = request.POST.get('address_id')
    print(address_id)
    delete_address = Address.objects.get(id=address_id).delete()
    return JsonResponse({'status': 'done'})


#########################################################################################################################

@csrf_exempt
def user_paypal_place_order(request):
    request.session['checkout_status'] = 'False'
    status = ''
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        address_id = request.POST.get('address_id')
        this_user = Users.objects.get(email=user)
        cart_products = Cart.objects.filter(user=this_user.id)
        for product in cart_products:
            this_product = Products.objects.get(id=product.product_id)
            new_order = Orders.objects.create(product=this_product, user=this_user, quantity=product.quantity,
                                              Address=address_id, total_price=product.total_price,
                                              payment_method=payment_method)
            print('adding : ', this_product.name)
            new_order.save()
            cart_products = Cart.objects.filter(user=this_user.id).delete()
        status = 'success'
        return JsonResponse({'status': status})


#########################################################################################################################

@never_cache
@csrf_exempt
def user_razorpay_place_order(request):
    '''handles payment gateway - razorpay'''
    # request.session['checkout_status'] = 'False'
    status = ''
    # sub_total = request.session['sub_total']
    sub_total = 234
    print(sub_total)
    if request.method == 'POST':
        user = request.POST.get('user')
        payment_method = request.POST.get('payment_method')
        this_user = Users.objects.get(email=user)
        cart_products = Cart.objects.filter(user=this_user.id)
        for product in cart_products:
            this_product = Products.objects.get(id=product.product_id)
            new_order = Orders.objects.create(product=this_product, user=this_user, quantity=product.quantity,
                                              Address=1, total_price=product.total_price, payment_method=payment_method)
            print('adding : ', this_product.name)
            new_order.save()
            cart_products = Cart.objects.filter(user=this_user.id).delete()
            status = 'success'
    return redirect('/user_thankyou_for_order')


#############################################################################################################################   

@csrf_exempt
def razorpay_success(request):
    return render(request, 'success.html')


#############################################################################################################################


@never_cache
def user_thankyou_for_order(request):
    # thankyou(request)
    request.session['checkout_status'] = 'False'
    print(request.session['checkout_status'])
    return render(request, 'user_thankyou_for_order.html')


#########################################################################################################################


@never_cache
def user_category_view(request, name):
    '''Render and Control the user category view'''
    if 'user' in request.session:
        user = request.session['user']
        this_user = Users.objects.get(email=user)
    else:
        user = 'guest'
        this_user = 'guest'
    global cart_count
    price_filter_min = 0
    price_filter_max = 10000
    category = Category.objects.get(name=name)
    category_products = Products.objects.filter(category=category.name)
    categories = Category.objects.all()
    product_count = category_products.count()
    p = Paginator(category_products, 2)
    pages = ''
    page_obj = p.get_page(1)
    if 'page' in request.session:
        page_number = request.session['page']
        page_obj = p.get_page(page_number)
    if request.method == 'POST':
        if 'task' in request.POST.keys():
            task = request.POST.get('task')
            if task == 'price_filter':
                minmum_price = request.POST.get('minimum')
                maximum_price = request.POST.get('maximum')
                print(maximum_price, minmum_price)
                category_products = Products.objects.filter(category=category.name,
                                                            price__range=(minmum_price, maximum_price))
                p = Paginator(category_products, 2)
                price_filter_min = minmum_price
                price_filter_max = maximum_price
        page_number = request.POST.get('page')
        try:
            page_obj = p.get_page(page_number)
            request.session['page'] = page_number
            print('page changed')  # returns the desired page object
        except:
            page_obj = p.get_page(1)
    for i in range(0, p.num_pages):
        print(i)
        pages = pages + '.'
    context = {
        'category': category,
        'category_products': page_obj,
        'categories': categories,
        'pages': pages,
        'min': price_filter_min,
        'max': price_filter_max,
        'cart_count': cart_count,
        'user': this_user,
    }
    return render(request, 'user_category_view.html', context)


# end
#############################################################################################################################
def user_products(request):
    global cart_count
    '''Render and control the datas in the user home page'''
    user = ''
    try:
        if 'user' in request.session:
            user_email = request.session['user']
            user = Users.objects.get(email=user_email)
            cart_count = Cart.objects.filter(user=user).count()
        else:
            user = 'guest'
            guest_id = request.COOKIES['sessionid']
            cart_count = Cart.objects.filter(guest_id=guest_id).count()
    except:
        pass
    try:
        banner1 = Banners.objects.get(id=1)  # getting the banner data
        banner2 = Banners.objects.get(id=2)  # getting the banner data
        banner3 = Banners.objects.get(id=3)  # getting the banner data
    except:
        banner1 = ''  # assigning null to the banners if there is an issue in getting the banner
        banner2 = ''  # assigning null to the banners if there is an issue in getting the banner
        banner3 = ''  # assigning null to the banners if there is an issue in getting the banner
    try:
        products = Products.objects.all()
        trusted_products = Products.objects.filter(is_trusted='trusted')
        best_offer_products = Products.objects.all()
        rated_products = Products.objects.filter(rating=5)
    except:
        products = ''
    try:
        categories = Category.objects.all()
    except:
        categories = ''
    print(products)
    context = {
        'user': user,
        'banner1': banner1,
        'banner2': banner2,
        'banner3': banner3,
        'products': products,
        'categories': categories,
        'trusted_products': trusted_products,
        'best_offer_products': best_offer_products,
        'rated_products': rated_products,
        'cart_count': cart_count,
    }
    return render(request, 'user_products.html', context)


#########################################################################################################################@never_cache

def admin_get_graph_data(request):
    admin = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    sales_graph_data = []
    sales_graph_category = []
    user_graph_data = []
    user_graph_category = []
    if request.method == 'POST':
        duration = request.POST.get('duration')
        print('Getting Graph details of ', duration)
        orders = Orders.objects.all()
        users = Users.objects.all()
        if duration == 'today':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            # finding the number of sales on today based on orders
            cycle = 0
            for sale in orders:
                cycle = cycle + 1
                # filtering sales based on year
                if str(sale.Order_year) == str(current_date.year):
                    # filtering sales based on month
                    if str(sale.Order_month) == str(current_date.month):
                        # filtering sales based on day
                        if str(sale.Order_day) == str(current_date.day):
                            # filterin sales which has the status as delivered based on orders
                            print(sale.status)
                            if str(sale.status == 'delivered'):
                                count = count + 1
                            sales_graph_data.append(count)
                            sales_graph_category.append(cycle)
            # printing the number of sales on today
            print('Number of sales In Today Is ', count)
            for user in users:
                # filtering sales based on year
                if str(user.signup_year) == str(current_date.year):
                    # filtering sales based on month
                    if str(user.signup_month) == str(current_date.month):
                        # filtering sales based on day
                        if str(user.signup_day) == str(current_date.day):
                            count = count + 1
                            user_graph_data.append(4)
                            user_graph_category.append(1)
        elif duration == 'last_7_days':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            # getting the sales of last  days
            # value of day is from 1 to 7
            for day in range(0, 7):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        # print(sale.Order_day,current_date.day-timedelta(days=day).days)
                        if str(sale.Order_day) == str(current_date.day - (timedelta(days=day).days)):
                            # print('count+',count)
                            count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(current_date.day - (timedelta(days=day).days))
            print('Number of sales in the last 7 days is ', sales_graph_data)
            # getting the new users
            for day in range(0, 7):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(current_date.month):
                            # print(sale.Order_day,current_date.day-timedelta(days=day).days)
                            if str(user.signup_day) == str(current_date.day - (timedelta(days=day).days)):
                                # print('count+',count)
                                count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(current_date.day - (timedelta(days=day).days))
            print('Number of revenue in the last 7 days is ', user_graph_data)
        # this month
        elif duration == 'last_month':
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            for day in range(1, 32):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        if str(sale.Order_month) == str(current_date.month):
                            if str(sale.Order_day) == str(day):
                                count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(day)
            for day in range(1, 32):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(current_date.month):
                            if str(user.signup_day) == str(day):
                                count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(day)
        # this year
        else:
            sales_graph_data = []
            sales_graph_category = []
            user_graph_data = []
            user_graph_category = []
            count = 0
            for month in range(1, 13):
                count = 0
                for sale in orders:
                    if str(sale.Order_year) == str(current_date.year):
                        if str(sale.Order_month) == str(month):
                            count = count + 1
                sales_graph_data.append(count)
                sales_graph_category.append(month)
            for month in range(1, 13):
                count = 0
                for user in users:
                    if str(user.signup_year) == str(current_date.year):
                        if str(user.signup_month) == str(month):
                            count = count + 1
                user_graph_data.append(count)
                user_graph_category.append(month)
    user_count = Users.objects.all().count()
    sales = Orders.objects.filter(status='Delivered')
    cod = Orders.objects.filter(payment_method='cod').count()
    paypal = Orders.objects.filter(payment_method='paypal').count()
    razorpay = Orders.objects.filter(payment_method='razorpay').count()
    paypal_payment_method_graph_data = paypal
    razorpay_payment_method_graph_data = razorpay
    cod_payment_method_graph_data = cod
    revenue = 0
    for sale in sales:
        revenue = revenue + sale.total_price
    return render(request, 'admin_panel.html', {
        'duration': duration,
        'customer_count': user_count,
        'sales': sales.count(),
        'revenue': revenue,
        'admin': this_admin,
        'sales_graph_data': sales_graph_data,
        'sales_graph_category': sales_graph_category,
        'user_graph_data': user_graph_data,
        'user_graph_category': [user_graph_category],
        'paypal_payment_method_graph_data': paypal_payment_method_graph_data,
        'razorpay_payment_method_graph_data': razorpay_payment_method_graph_data,
        'cod_payment_method_graph_data': cod_payment_method_graph_data,
    })


#######################################################################################################################


@never_cache
def user_invoice(request):
    '''This function will manage the user invoice '''
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 10)
    this_user = Users.objects.get(email=user)
    order_details = Orders.objects.filter(
        user=this_user.id, status='Delivered')
    lines = [
        'Sales Report of Aldrich Shopping ',
        '',
        '      Date      |       brand       |                       product name                     |  sold   |   stock balance  |   revenue  ',
        '',

    ]
    for orders in order_details:
        lines.append(str(orders.Order_day) +
                     str('/' + str(orders.Order_month)) +
                     str('/' + str(orders.Order_year)) +
                     str('         ' + str(orders.product.category)) +
                     str('        ' + str(orders.product.name)) +
                     str('       ' + str(orders.product.total_sold)) +
                     str('            ' + str(orders.product.stock_available)) +
                     str('                 ' + str(orders.product.price))

                     )

        lines.append(
            "-----------------------------------------------------------------------------------------------------------------------------------")
    lines.append('')
    lines.append('This report is of the duration of last 7 days')
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Adrich_User_invoice.pdf')


# end
#############################################################################################################################


@never_cache
def user_invoice_per_item(request, id):
    '''handle user invoice per item'''
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 10)
    this_user = Users.objects.get(email=user)
    order_details = Orders.objects.get(id=id)
    lines = [
        'INVOICE ',
        '',
        '',
        '',
        'Customer Name : {username}'.format(username=this_user.full_name),
        '',
        'Contact : {contact}'.format(contact=this_user.contact_number),
        '',
        '----------------------------------------------------------------------------------------------------------------------------------------------',
        '',
        'Product ID: {product_id}'.format(
            product_id=order_details.product.id),
        '',
        'Product Name: {product_name}'.format(
            product_name=order_details.product.name),
        '',
        'Order Status : {order_status}'.format(
            order_status=order_details.status),
        '',
        '',
        '',
        'Provided Discount : {discount} %'.format(
            discount=int(order_details.product.offer_percentage)),
        '',
        'Total Price : Rs {product_price}'.format(
            product_price=order_details.total_price),
        '',
    ]
    lines.append('')
    lines.append('Thank you for Shoping with us.')
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    print(buf)
    return FileResponse(buf, as_attachment=True, filename='aldrich_invoice.pdf')


# end
#############################################################################################################################

@never_cache
def admin_sales_report(request):
    ppp = 5  # product per page in sales report
    current_page = 1
    global duration, orders
    current_report_day = current_date.day
    current_report_month = current_date.month
    current_report_year = current_date.year
    admin = ''
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    this_admin = Users.objects.get(email=admin)
    if 'duration' in request.POST.keys():
        orders = Orders.objects.all()
        if 'page_number' in request.POST.keys():
            current_page = request.POST.get('page_number')
            print('got page_number', current_page)
        duration = request.POST.get('duration')
        print(duration)
        if duration == 'custom_search':
            from_date = request.POST.get('from')
            to_date = request.POST.get('to')
            from_date = from_date.split('-')
            to_date = to_date.split('-')
            from_day = from_date[2]
            from_month = from_date[1]
            from_year = from_date[0]
            to_day = to_date[2]
            to_month = to_date[1]
            to_year = to_date[0]
            print('trying to filter the sales report from the date', from_day, '/', from_month, '/', from_year, ' to ',
                  to_day, '/', to_month, '/', to_year)
            for order in orders:
                orders = Orders.objects.filter(
                    Order_day__gte=int(from_day),
                    Order_month__gte=int(from_month),
                    Order_year__gte=int(from_year),
                    Order_day__lte=int(to_day),
                    Order_month__lte=int(to_month),
                    Order_year__lte=int(to_year),
                )
            p = Paginator(orders, ppp)
            page_obj = p.get_page(current_page)
            available_pages = []
            pages = int(orders.count() / ppp)
            for i in range(pages):
                available_pages.append(i)
            return render(request, 'admin_sales_report.html', {
                'admin': this_admin,
                'orders': page_obj,
                '10_year_back': int(current_date.year) - 9,
                'duration': duration,
                'current_date': current_date,
                'available_pages': available_pages,
                'current_report_day': 0,
                'current_report_month': 0,
                'current_report_year': 0,
                'current_page': current_page,
            })
        if 'current_report_year' in request.POST.keys():
            picked_year = request.POST.get('current_report_year')
            picked_month = request.POST.get('current_report_month')
            picked_date = request.POST.get('current_report_day')
            current_report_year = int(picked_year)
            current_report_month = int(picked_month)
            current_report_day = int(picked_date)
            orders = Orders.objects.filter(Order_year=picked_year, Order_month=picked_month, Order_day=picked_date)
        p = Paginator(orders, ppp)
        page_obj = p.get_page(current_page)
        available_pages = []
        pages = int(orders.count() / ppp)
        for i in range(pages):
            available_pages.append(i)
        return render(request, 'admin_sales_report.html', {
            'admin': this_admin,
            'orders': page_obj,
            '10_year_back': int(current_date.year) - 9,
            'duration': duration,
            'current_date': current_date,
            'available_pages': available_pages,
            'current_report_day': current_report_day,
            'current_report_month': current_report_month,
            'current_report_year': current_report_year,
            'current_page': current_page,
        })
    elif 'export' in request.POST.keys():
        filetype = request.POST.get('filetype')
        if filetype == 'pdf':
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
            textob = c.beginText()
            textob.setTextOrigin(inch, inch)
            textob.setFont("Helvetica", 10)
            lines = [
                'Sales Report of Aldrich Shopping ',
                'This Report is Generated by aldrichshopping',
                '',
                '',
                '',
            ]
            for order in orders:
                print(order.product.name)
                lines.append(
                    str(str(order.product.name)) +
                    str('    ' + str(order.Order_day)) +
                    str('/' + str(order.Order_month)) +
                    str('/' + str(order.Order_year)) +
                    str('         ' + str(order.product.category)) +
                    str('                 ' + str(order.product.price))
                )
                lines.append(
                    "-----------------------------------------------------------------------------------------------------------------------------------")
            lines.append('')
            lines.append('Have a Nice Day!')
            for line in lines:
                textob.textLine(line)
            c.drawText(textob)
            c.showPage()
            c.save()
            buf.seek(0)
            return FileResponse(buf, as_attachment=True, filename='output.pdf')
        elif filetype == 'csv':
            # output filename handling
            filename = 'Aldrich Report'
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
                filename)
            writer = csv.writer(response)
            writer.writerow(['Product Name', 'Ordered Day', 'Ordered Month',
                             'Ordered Year', 'Quantity', 'Total Price'])
            if duration == 'Today':
                ordered_products = Orders.objects.filter(
                    Order_day=current_date.day)
            if duration == 'Month':
                ordered_products = Orders.objects.filter(
                    Order_month=current_date.month)
            if duration == 'Year':
                ordered_products = Orders.objects.filter(
                    Order_year=current_date.year)
            for product in ordered_products:
                print(product.product.name)
                print(product.Order_day, product.Order_month,
                      product.Order_year)
                print(product.quantity)
                print(product.total_price)
                row = [product.product.name, product.Order_day, product.Order_month,
                       product.Order_year, product.quantity, product.total_price]
                writer.writerow(row)
            return response
    orders = Orders.objects.all()
    p = Paginator(orders, ppp)
    page_obj = p.get_page(1)
    available_pages = []
    pages = int(orders.count() / ppp)
    for i in range(pages):
        available_pages.append(i)
    return render(request, 'admin_sales_report.html', {
        'admin': this_admin,
        'orders': page_obj,
        'current_date': current_date,
        '10_year_back': int(current_date.year) - 9,
        'duration': duration,
        'available_pages': available_pages,
        'current_report_day': current_date.day,
        'current_report_month': current_date.month,
        'current_report_year': current_date.year,
        'current_page': current_page,
    })
    # end


####################################################################
def user_export_myorders_in_csv(request):
    '''this function will export the files in myorders as csv'''
    # Create the HttpResponse object with the appropriate CSV header.
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    this_user = Users.objects.get(email=user)
    # output filename handling
    filename = str(this_user.full_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        filename)
    writer = csv.writer(response)
    ordered_products = Orders.objects.filter(user=this_user.id)
    for product in ordered_products:
        print(product.product.name)
        print(product.Order_day, product.Order_month, product.Order_year)
        print(product.quantity)
        print(product.total_price)
        row = [product.product.name, product.Order_day, product.Order_month,
               product.Order_year, product.quantity, product.total_price]
        writer.writerow(row)
    return response


###################################################################
@never_cache
@never_cache
def user_validate_coupon(request):
    '''handle the coupon validation'''
    request.session['checkout_status'] = 'False'
    discount = 0
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    this_user = Users.objects.get(email=user)
    if request.method == 'POST':
        entered_coupon = request.POST.get('coupon')
        discount_percentage = 0
        available_coupons = Coupon.objects.all()
        status = 'failed'
        for coupon in available_coupons:
            if coupon.coupon == entered_coupon:
                coupon_history = Coupon_history.objects.all()
                for coupon_detail in coupon_history:
                    if int(this_user.id) == int(coupon_detail.user_id):
                        if entered_coupon == coupon_detail.coupon_code:
                            status = 'used'
                            return JsonResponse({'status': status})
                used_coupon = Coupon_history.objects.create(
                    user_id=this_user.id, coupon_code=entered_coupon)
                used_coupon.save()
                print('Coupon Applied')
                discount_percentage = coupon.discount_percentage
                status = 'success'
        prize = int(request.session['sub_total'])
        print(prize)
        discount = int(prize) * (discount_percentage / 100)
        discount_price = int(
            request.session['sub_total'] - discount)
        request.session['sub_total'] = discount_price
    return JsonResponse({'discount': discount_price, 'status': status})


# end
#############################################################################################################################
@never_cache
def admin_remove_coupon(request):
    if request.method == 'POST':
        print('trying to remove')
        coupon_id = request.POST.get('coupon_id')
        coupon = Coupon.objects.get(id=coupon_id).delete()
        print('coupon deleted')
        return JsonResponse({'status': 'done'})
    coupons = Coupon.objects.all()
    return render(request, 'admin_manage_coupons.html', {'coupons': coupons})


@never_cache
def admin_add_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('new_coupon')
        coupon_discount = request.POST.get('new_coupon_discount')
        print('trying to add a new coupon')
        new_coupon = Coupon.objects.create(
            coupon=coupon_code, discount_percentage=coupon_discount)
        new_coupon.save()
        print(' coupon added ')
        return JsonResponse({'status': 'success'})


@csrf_exempt
def razorpay_success(request):
    return render(request, 'success.html')


def test(request):
    if request.method == 'POST':
        print('received_image')


#######################################################################################


@never_cache
def admin_category_offers(request):
    admin = ''
    ppp = 5
    current_page = 1
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    if 'page_number' in request.POST.keys():
        current_page = request.POST.get('page_number')
    elif request.method == 'POST':
        new_offer_percentage = request.POST.get('new_offer_percentage')
        category_id = request.POST.get('category_id')
        print(new_offer_percentage, category_id)
        category = Category.objects.get(id=category_id)
        category.offer_percentage = new_offer_percentage
        category.save()
    this_admin = Users.objects.get(email=admin)
    categories = Category.objects.all()
    p = Paginator(categories, ppp)
    page_obj = p.get_page(current_page)
    available_pages = []
    pages = int(categories.count() / ppp)
    for i in range(pages):
        available_pages.append(i)
    context = {
        'categories': page_obj,
        'available_pages': available_pages,
        'current_page': current_page
    }
    return render(request, 'admin_category_offers.html', context)


#########################################################################

@never_cache
def admin_product_offers(request):
    admin = ''
    ppp = 5
    current_page = 1
    if 'admin' in request.session:
        admin = request.session['admin']
    else:
        return redirect('/admin_sign_in')
    if 'page_number' in request.POST.keys():
        current_page = request.POST.get('page_number')
    elif request.method == 'POST':
        new_offer_percentage = request.POST.get('new_offer_percentage')
        product_id = request.POST.get('product_id')
        print(new_offer_percentage, product_id)
        product = Products.objects.get(id=product_id)
        product.offer_percentage = new_offer_percentage
        product.save()
    this_admin = Users.objects.get(email=admin)
    products = Products.objects.all()
    p = Paginator(products, ppp)
    page_obj = p.get_page(current_page)
    available_pages = []
    pages = int(products.count() / ppp)
    for i in range(pages):
        available_pages.append(i)
    context = {
        'products': page_obj,
        'available_pages': available_pages,
        'current_page': current_page
    }
    return render(request, 'admin_product_offers.html', context)


#########################################################################

@never_cache
def user_return_order(request, order_id):
    '''handles the return request from the user'''
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    this_user = Users.objects.get(email=user)
    product = Orders.objects.get(id=order_id)
    if request.method == 'POST':
        user = this_user.id
        reason = request.POST.get('reason')
        return_request = Return_request.objects.create(
            user=this_user, reason=reason)
        return_request.save()
        product.status = 'return requested'
        product.save()
        print('return request applied ')
        return redirect('/user_account')
    return render(request, 'user_return_order_form.html', {'product': product})


# end

###########################################################################

@never_cache
def forget_password(request):
    return render(request, 'forget_password.html')


###########################################################################

@never_cache
def user_pay_with_wallet(request):
    '''handle payment gateway - wallet'''
    status = 'insufficiant balance'
    if 'user' in request.session:
        user = request.session['user']
    else:
        return redirect('/user_sign_in')
    this_user = Users.objects.get(email=user)
    if request.method == 'POST':
        sub_total = request.POST.get('sub_total')
        wallet_balance = int(this_user.wallet_balance)
        payment_method = 'wallet'
        cart_products = Cart.objects.filter(user=this_user.id)
        print(sub_total, wallet_balance)
        if int(sub_total) > int(wallet_balance):
            status = 'insufficiant_balance'
        else:
            for product in cart_products:
                this_product = Products.objects.get(id=product.product_id)
                new_order = Orders.objects.create(product=this_product, user=this_user, quantity=product.quantity,
                                                  Address=1, total_price=product.total_price,
                                                  payment_method=payment_method)
                print('adding : ', this_product.name)
                new_order.save()
                new_to_wallet = Wallet_history.objects.create(user_id=this_user.id, order_id=new_order,
                                                              Debit_Credit='debited')
                new_to_wallet.save()
                this_user.wallet_balance = int(this_user.wallet_balance) - int(product.total_price)
                this_user.save()
                cart_products = Cart.objects.filter(user=this_user.id).delete()
                status = 'success'
        print('got wallet amount')
        return JsonResponse({'status': status})
    return render(request, 'user_pay_with_wallet.html')


######################################################################
@never_cache
def add_to_wallet_history(order):
    '''helps to add the amount to the wallet'''
    new_wallet_history = Wallet_history.objects.create(order_id=order)
    new_wallet_history.save()


######################################################################
@never_cache
def user_wallet(request):
    '''handle the user wallet requests'''
    global cart_count
    if 'user' in request.session:
        user = request.session['user']
        this_user = Users.objects.get(email=user)
    else:
        return redirect('/user_sign_in')
    if request.method == 'POST':
        user_entered_amount = request.POST.get('user_entered_amount')
        this_user.wallet_balance = int(this_user.wallet_balance) + int(user_entered_amount)
        this_user.save()
        print(user_entered_amount)
    user = Users.objects.get(email=user)
    wallet_balance = user.wallet_balance
    user_wallet_history = Wallet_history.objects.filter(user_id=this_user.id)
    context = {
        'wallet_balance': wallet_balance,
        'user_wallet_history': user_wallet_history,
        'user': this_user,
        'cart_count': cart_count,
    }
    return render(request, 'user_wallet.html', context)
