from django import forms
from base.models import Product

class addproduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','brandname','mainprice','price','category','colour','discription','image')
        # fields = ('name','price','image')

from django.contrib.auth.forms import SetPasswordForm

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        
        # Remove password validation constraints
        self.fields['new_password1'].widget.attrs.pop("min_length", None)
        self.fields['new_password2'].widget.attrs.pop("min_length", None)
        self.fields['new_password1'].widget.attrs.pop("validate_password", None)