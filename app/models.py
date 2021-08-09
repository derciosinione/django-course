from django.db import models
from django.contrib.auth.models import User

class Friends(models.Model):
  name = models.CharField(max_length=50, null=False, blank=False)
  age = models.IntegerField(default=0)
  email = models.EmailField(max_length=50, unique=True, blank=False, null=False)
  userid = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

  def __str__(self) -> str:
      return f'{self.name} - {self.userid.username}'