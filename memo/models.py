from django.db import models
from django.core.cache import cache


class Memo(models.Model):
    created_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=200)    

    class Meta:
        ordering = ['-id']
        db_table = 'memo'

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        cache.delete('memos')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete('memos')
        super().delete(*args, **kwargs)
