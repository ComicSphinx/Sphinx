from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# TODO refactor it, at least name
class Budget(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    field_name = models.TextField(default='null')
    field_value = models.TextField(default='null') # TODO сделать это поле числовым, вместе с инпутом(чтобы принимал только числа)
    active = models.BooleanField()