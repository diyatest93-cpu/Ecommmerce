from django import forms
from .models import *

class categoryForm(forms.ModelForm):
    
    class Meta:
        model = category
        fields = ['category_name', 'category_image','status']

class subcategoryForm(forms.ModelForm):
    class Meta:
        model=subcategory
        fields=['category', 'subcategory_name','subcategory_image' ,'status']
        widgets={'category':forms.Select(attrs={'class':'form-select'}),
                 'subcategory_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Subcategory name'}),
                 'status':forms.CheckboxInput(attrs={'class':'form-check-input'})}


class thirdcategoryForm(forms.ModelForm):
    class Meta:
        model=thirdcategory
        fields=['subcategory', 'thirdcategory_name','thirdcategory_image', 'status']
        widgets={'subcategory':forms.Select(attrs={'class':'form-select'}),
                 'thirdcategory_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Thirdcategory Name'}),
                 'status':forms.CheckboxInput(attrs={'class':'form-check-input'})}

        
class productForm(forms.ModelForm):
    class Meta:
        model=product
        fields=['category', 'subcategory', 'thirdcategory', 'pname', 'brand','price','p_detail', 'p_image', 'p_rating', 'status', 'stock']

        widgets={'category':forms.Select(attrs={'class':'form-select'}),
                 'subcategory':forms.Select(attrs={'class':'form-select'}),
                 'thirdcategory':forms.Select(attrs={'class':'form-select'}),
                 'pname':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Product Name'}),
                 'brand':forms.TextInput(attrs={'class':'form-control', "placeholder":'Enter brand name'}),
                 'price':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter Price'}),
                 'p_detail':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Product detail'}),
                 'p_image':forms.ClearableFileInput(attrs={'class':'form-control'}),
                 'p_rating':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter rating'}),
                 'status':forms.CheckboxInput(attrs={'class':'form-check-input'}),
                 'stock':forms.NumberInput(attrs={'class':'form-control', 'placegolder':'enter product stock'})

        }

class bannerForm(forms.ModelForm):
    class Meta:
        model=banner
        fields=['b_title', 'b_detail', 'b_image', 'button_text', 'button_link', 'status']
        widgets={'b-title':forms.TextInput(attrs={'class':'form-control'}),
                 'b_detail':forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter detail', 'rows':3}),
                 'b_image':forms.ClearableFileInput(attrs={'class':'form-control'}),
                 'button_text':forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter button text'}),
                 'button_link':forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter button link'}),
                 'status':forms.CheckboxInput(attrs={'class':'form-control'}),
                 }

class addressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields = [
            'full_name',
            'mobile_no',
            'address',
            'city',
            'state',
            'pincode',
        ]
        widgets={'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Full Name'}),
                 'mobile_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter MobileNo'}),
                 'address':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Full Address'}),
                 'city':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter City'}),
                 'state':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter state'}),
                 'pincode':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter pincode'})}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']

        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'placeholder': 'Give rating 1-5'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review...'
            }),
        }