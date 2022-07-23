from django.db import models

class BudgetFields(models.Model):
    # + userId (связать, когда появится авторизация и userid, я буду их где-то хранить) TODO: создать класс "пользователь"
    name = models.CharField(max_length=100)
    active = models.BooleanField()


class Budget(models.Model):
    # + userId (связать, когда появится авторизация и userid, я буду их где-то хранить) TODO: создать класс "пользователь"
    budgetFieldId = models.ForeignKey(BudgetFields, on_delete=models.PROTECT)
    value = models.CharField(max_length=100)
    active = models.BooleanField()