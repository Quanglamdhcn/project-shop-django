from django import forms 
from .models import Product, SIZE_CHOICES, Photo

class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ('file', )

class ProductFormCreate(forms.ModelForm):
	size = forms.MultipleChoiceField(choices=SIZE_CHOICES)
	
	class Meta:
		model = Product
		fields = ['name','size','description','price']