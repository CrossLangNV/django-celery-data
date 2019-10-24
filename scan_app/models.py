from django.db import models

class TextFile(models.Model):
    name = models.CharField(max_length=200)
    line_count = models.IntegerField(default=0)

    def __str__(self):
        return "TextFile(name=%s, line_count=%d)" % (self.name, self.line_count)