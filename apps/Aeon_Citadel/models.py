from django.db import models


class Journey(models.Model):
    avatar_id = models.CharField(max_length=128, primary_key=True, default='0')
    avatar_name = models.CharField(max_length=128)
    avatar_status = models.CharField(max_length=128, default='{}')
    event = models.CharField(max_length=512, default="")
    difficulty = models.IntegerField(max_length=4, default=1)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.avatar_name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "角色"
        verbose_name_plural = "角色"
