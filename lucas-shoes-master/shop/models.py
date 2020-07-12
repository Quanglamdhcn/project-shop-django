from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from PIL import Image



class Photo(models.Model):
	product = models.ForeignKey(to="Product",on_delete=models.CASCADE,related_name='photos')
	file = models.FileField(upload_to='products/')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ("-uploaded_at",)

	def save(self, *args, **kwargs):
		super(Photo, self).save(*args, **kwargs)
		
		img = Image.open(self.file.path)
		image = img.resize((458,617), Image.ANTIALIAS)
		image.save(self.file.path)

SIZE_CHOICES = [(i,str(i)) for i in range(36,46)]

class Product(models.Model):
	name = models.CharField(('Tên sản phẩm'),max_length=100)
	slug = models.SlugField(max_length=100,unique=True, blank=True)
	size = MultiSelectField(choices =SIZE_CHOICES)
	description = models.TextField(('Miêu tả'), blank=True)
	price = models.IntegerField()
	views = models.PositiveIntegerField(default=0)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created','name')
		index_together = (('id','slug'),)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug= slugify(self.name)
		super(Product,self).save(*args,**kwargs)

	
