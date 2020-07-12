from django import forms
from django.shortcuts import get_object_or_404
from shop.models import Product
from shop.models import SIZE_CHOICES


PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
	quantity = forms.TypedChoiceField(
		choices=PRODUCT_QUANTITY_CHOICES,
		initial=1,
		coerce=int, label='SL'
	)
	size = forms.TypedChoiceField(
		choices= SIZE_CHOICES,
		initial=36,
		coerce=int
	)
	update_quantity = forms.BooleanField(
		required=False,
		initial=False,
		widget=forms.HiddenInput
	)

	def __init__(self,product_id=None,*args, **kwargs):
		super(CartAddProductForm,self).__init__(*args, **kwargs)
		if product_id:
			product = get_object_or_404(Product, id=product_id)
			SIZE_CHOICES = [(i,str(i)) for i in product.size]

			self.fields['size'] =  forms.TypedChoiceField(
				choices= SIZE_CHOICES,
				initial=SIZE_CHOICES[0],
				coerce=int
			)