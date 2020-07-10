from django.db import models
from users.models import User
from datetime import datetime

# Create your models here.
class Habit(models.Model):
    action = models.CharField(max_length=50)
    lesser = models.BooleanField(choices=[(False, 'More Than'), (True, 'Less Than')], default=False)
    goal = models.FloatField()
    unit = models.CharField(max_length=50)
    period = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")

class Record(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="records")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="records")
    goal_met = models.BooleanField()
    quantity = models.FloatField()
    added = models.DateField(default=datetime.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['habit', 'added'], name='unique record')
        ]