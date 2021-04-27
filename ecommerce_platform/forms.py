from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm
from ecommerce_platform.models import *
import sys
from django.core.validators import validate_email

MAX_UPLOAD_SIZE = sys.maxsize


# Login and registration forms from homework
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=50,
                                       widget=forms.PasswordInput())
    email = forms.CharField(max_length=50, widget=forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        validate_email(cleaned_data.get('email'))

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["review_content"]

    def clean(self):
        return super().clean()


def clean_picture(picture):
    if not picture or not hasattr(picture, 'content_type'):
        raise forms.ValidationError('You must upload a picture')
    if not picture.content_type or not picture.content_type.startswith(
            'image'):
        raise forms.ValidationError('File type is not image')
    if picture.size > MAX_UPLOAD_SIZE:
        raise forms.ValidationError(
            'File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
    return picture


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "product_picture1", "product_picture2",
                  "product_picture3", "product_price", "product_description",
                  "product_in_stock_quantity", "product_category"]

    def clean(self):
        return super().clean()

    def clean_product_picture1(self):
        picture1 = self.cleaned_data['profile_picture1']
        return clean_picture(picture1)

    def clean_product_picture2(self):
        picture2 = self.cleaned_data['profile_picture2']
        return clean_picture(picture2)

    def clean_product_picture3(self):
        picture3 = self.cleaned_data['profile_picture3']
        return clean_picture(picture3)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

    def clean_profile_picture(self):
        picture = self.cleaned_data['profile_picture']
        return clean_picture(picture)
