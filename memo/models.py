from django.db import models

class Memo(models.Model):
    created_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        ordering = ['-id']
        db_table = 'memo'

    def __str__(self):
        return '{}'.format(self.title)
