from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# TODO refactor it, at least name
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    active = models.BooleanField()

    def serialize(self):
        # TODO сделать так, чтобы возвращались только активные (если я не сделаю это в шаблоне)
        return {
            'user': self.user,
            'field_name': self.field_name,
            'value': self.value,
            'active': self.active
        }