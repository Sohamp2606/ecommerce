# import base64
from functools import reduce
import io
# import operator
from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from base.forms import addproduct
from django.contrib import messages
from base.models import Product
import qrcode
from django.contrib.auth import authenticate as auth_authenticate, login as auth_login
from django.core.mail import send_mail
from django.http import HttpResponse

# from django.core.files.base import ContentFile

# Create your views here.
def home(request):
    return render(request,'home.html')


def register(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request,'Username already taken')
            return redirect('register')
        
        user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username
           )
        user.set_password(password)
        user.save()
        return redirect('home')

    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = auth_authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def upload_from(request):
    if request.method == 'POST':
        
        form = addproduct(request.POST,request.FILES)
       
        if form.is_valid():
            
            form.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = addproduct()     
    context = {'form':addproduct}
    return render(request,'addproduct.html',context)

def products(request):

    price_ranges = {
    'range1': 'Under 1,000 Rs',
    'range2': '1,000 Rs - 10,000 Rs',
    'range3': '10,000 Rs - 30,000 Rs',
    'range4': '30,000 Rs - 60,000 Rs',
    'range5': 'Over 60,000 Rs',
    }
    

    search_input = request.POST.get('search-area')
    category_filter = request.GET.get('category') or request.POST.get('category')
    sort_by = request.GET.get('sort') or request.POST.get('sort')
    price_range_filter = request.POST.getlist('price_range')
   
    allproducts = Product.objects.all()
    if search_input:
        allproducts = Product.objects.filter(name__contains=search_input)
    elif category_filter:
        allproducts = Product.objects.filter(category=category_filter)
    # else:
    #     allproducts = Product.objects.all()
    
    if price_range_filter:
        price_queries =[]
        for price_range in price_range_filter:
            if price_range == 'range1':
                price_queries.append(Q(price__lt=1000))
            elif price_range == 'range2':
                price_queries.append(Q(price__range=(1000, 10000)))
            elif price_range == 'range3':
                price_queries.append(Q(price__range=(10000, 30000)))
            elif price_range == 'range4':
                price_queries.append(Q(price__range=(30000, 60000)))
            elif price_range == 'range5':
                price_queries.append(Q(price__gt=60000))
        if price_queries:
            price_filter = Q()
            for query in price_queries:
                price_filter |= query
            allproducts = allproducts.filter(price_filter)


    if sort_by == 'price_asc':
        allproducts = allproducts.order_by('price')
    elif sort_by == 'price_desc':
        allproducts = allproducts.order_by('-price')
    elif sort_by =='new_arrival':
        allproducts = allproducts.order_by('-arrival_date')
    if not search_input:
        search_input=''

    context ={
        'allproducts':allproducts,
        'search_input':search_input,
        'category':category_filter,
        'price_ranges':price_ranges,
    }
    return render(request,'products.html',context)


def payment2(request,price):
    payment_amount = price
    upi_id = "sohatil266@oksib"
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = f"upi://pay?pa={upi_id}&pn=CustomPayment&am={payment_amount}&cu=INR"
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create a BytesIO buffer to store the image data
    buffer = io.BytesIO()
    
    # Save the QR code image to the buffer
    try:
        qr.make_image(fill_color="black", back_color="white").save(buffer, "PNG")
        buffer.seek(0)
        
        # Read the image data from the buffer
        img_data = buffer.getvalue()
        
        # Set the content type for the HTTP response
        response = HttpResponse(img_data, content_type='image/png')
        return response
    except Exception as e:
        # Log the exception or print it for debugging
        print(f"Error generating QR code: {e}")
        return HttpResponse("Error generating QR code")

    
def qrimg(request,price):
    context={'price':price}
    return render(request,'payment.html',context)



from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# from django.contrib import messages

# from django.contrib.auth.models import User

def forgot_password(request):
    if request.method == 'POST':
       
        username = request.POST.get('username')
        email= request.POST.get('email')
        user = User.objects.filter(username=username).first()
        
        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
            
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {'reset_url': reset_url})
           
            from_email = 'sohampatil266@gmail.com'  # Replace with your email address
            to_email = email
            
            send_mail(subject, message, from_email, [to_email])

            return render(request, 'password_reset_sent.html')
        else:
            messages.error(request, 'This email is not associated with any account.')
    return render(request, 'password_reset_sent.html')


from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
# from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes

def reset_password_confirm(request, uidb64=None, token=None):
    print("\nstep1********")
    assert uidb64 is not None and token is not None  # Make sure both parameters are provided
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode the base64 encoded UID
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print("\nstep2********")
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                print("\nstep3********")
                # Optionally, log the user in after password reset
                user = auth_authenticate(request, username=user.username, password=request.POST['new_password1'])
                print("\nstep4********")
                if user is not None:
                    login(request, user)
                    return redirect('password_reset_complete')  # Redirect to password reset complete page
        else:
            form = SetPasswordForm(user)
        context = {
            'uidb64': uidb64,
            'token': token,
            'form': form,
        }
        return render(request, 'reset_password_confirm.html', context)
    else:
        return HttpResponseForbidden('Invalid password reset link')

def test2(request):
    
    return render(request,'test2.html')

def test_email(request):
    send_mail(
        'Test Email',
        'This is a test email from Django.',
        'sohampatil266@gmail.com.com',
        ['soham266official@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('Test email sent successfully.')







