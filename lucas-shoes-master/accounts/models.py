from django.db import models

class Contact(models.Model):
	name = models.CharField('Tên',max_length=30)
	email = models.EmailField('email',)
	title = models.CharField('Tiêu đề ',max_length=50)
	content = models.TextField('Nội dung nhắn gửi',)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('-created',)