from django import forms
from .models import Coupon

class CouponApplyForm(forms.Form):
	code = forms.CharField()

class CouponCreateForm(forms.ModelForm):
	valid_form = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
	valid_to = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
	class Meta:
		model = Coupon
		fields = ['code','valid_form','valid_to','discount','active']