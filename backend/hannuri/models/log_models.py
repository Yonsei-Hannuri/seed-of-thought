from django.db import models
from .app_models import *

class DetgoriReadTime(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="읽은 사람")
    detgori = models.ForeignKey(Detgori, on_delete=models.CASCADE, verbose_name="읽은 댓거리")
    duration = models.FloatField(blank=False, verbose_name="reading time")
    date = models.DateTimeField(auto_now_add=True, verbose_name="읽은 날짜")
        
    def __str__(self):
        return '{}에 {}가 {}를 {}초 동안 읽었습니다.'.format(self.date, self.reader, self.detgori, self.duration)

