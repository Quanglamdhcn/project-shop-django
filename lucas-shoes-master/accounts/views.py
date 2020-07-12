from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Contact
from .forms import ContactForm


def contact(request):
	form  = ContactForm()

	return render(request, 'accounts/contact.html', {'form':form,'section':'contact'})

@require_POST
def ajax_save_contact(request):
	data = {}
	form = ContactForm(request.POST)
	if form.is_valid():
		form.save()
		data['error'] = False

	else:
		data['error'] = True
		data['error_email'] = 'Email không hợp lệ'

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def contact_manage(request):
	contacts = Contact.objects.all()

	return render(request,'accounts/contact_manage.html',{'contacts':contacts})