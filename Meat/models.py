from django.db import models


class Meat(models.Model):
    """
    肉类（任务）
    """

    content = models.TextField(
        default=None,
        null=True,
    )
    toad = models.ForeignKey(
        'User.User',
        related_name='toad_user',
        on_delete=models.CASCADE,
    )
    target_time = models.DateTimeField(
        null=True
    )
    eaten = models.BooleanField(
        default=False
    )

# Create your models here.
