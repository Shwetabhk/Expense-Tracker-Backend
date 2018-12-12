import os
import random
from django.db import models
from users.models import User



def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name_ins = str(instance)
    _, ext = get_file_ext(filename)
    return "item_images/{name}{ext}".format(name=name_ins, ext=ext)

class Expense(models.Model):
	name = models.CharField(max_length=128)
	total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
	image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	date = models.DateField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.name.replace(" ", "_") + str(self.date)
