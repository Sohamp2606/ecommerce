
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('login/',views.login,name='login'),
    path('register/home/',views.home,name='registerhome'),
    path('register/',views.register,name='register'),
#     path('',views.register,name='register'),
    
    path('addproduct/',views.upload_from,name='addproduct'),
    
    path('payment/<int:price>/',views.qrimg,name='payment'),
    path('qrgenator/<int:price>/', views.payment2, name='payment5'),
    # path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
         name='password_reset'),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
           name='password_reset_complete'),

    path('mail/',views.test_email,name='test2'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
]
