from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# TODO refactor it, at least name
class Budget(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    field_name = models.TextField(default='null')
    field_value = models.BigIntegerField(default='null') # TODO сделать это поле числовым, вместе с инпутом(чтобы принимал только числа)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField()

class BudgetByMonths(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    field_id = models.ForeignKey(Budget, on_delete=models.CASCADE, null=False)
    field_name = models.TextField(default='null')
    field_value = models.BigIntegerField(default='null') # TODO сделать это поле числовым, вместе с инпутом(чтобы принимал только числа)
    month_number = models.TextField(default='null') # TODO сделать это поле числовым, (от 1 до 12)
    active = models.BooleanField() # TODO это поле надо деактивировать, если деактивировано поле active в Budget

class BudgetByYears(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    field_id = models.ForeignKey(Budget, on_delete=models.CASCADE, null=False)
    field_name = models.TextField(default='null')
    field_value = models.BigIntegerField(default='null') # TODO сделать это поле числовым, вместе с инпутом(чтобы принимал только числа)
    year_number = models.TextField(default='null') # TODO сделать это поле числовым
    active = models.BooleanField() # TODO это поле надо деактивировать, если деактивировано поле active в Budget