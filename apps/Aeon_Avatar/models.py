from django.db import models


class Avatar(models.Model):
    avatar_id = models.CharField(max_length=128, primary_key=True, default='0')
    user_id = models.CharField(max_length=128)
    name = models.CharField(max_length=128, unique=True)
    attack = models.CharField(max_length=128, default="0")
    defense = models.CharField(max_length=128, default="0")
    speed = models.CharField(max_length=128, default="0")
    range = models.CharField(max_length=128, default="0")
    magic = models.CharField(max_length=128, default="0")
    comment = models.TextField(default="")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "角色"
        verbose_name_plural = "角色"
