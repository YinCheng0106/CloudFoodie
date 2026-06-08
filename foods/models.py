from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Food(models.Model):

    CATEGORY_CHOICES = [
        ('chinese', '中式'),
        ('japanese', '日式'),
        ('korean', '韓式'),
        ('western', '西式'),
        ('dessert', '甜點'),
        ('drink', '飲料'),
        ('other', '其他'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='foods',
        verbose_name='建立者',
    )
    title = models.CharField('美食名稱', max_length=100)
    category = models.CharField(
        '分類', max_length=20, choices=CATEGORY_CHOICES, default='other'
    )
    address = models.CharField('地址', max_length=255, blank=True)
    note = models.TextField('個人筆記', blank=True)
    image = models.ImageField('照片', upload_to='foods/', blank=True, null=True)

    latitude = models.FloatField(
        '緯度',
        blank=True,
        null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.FloatField(
        '經度',
        blank=True,
        null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    ai_summary = models.TextField('AI 摘要', blank=True)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)

    class Meta:
        verbose_name = '美食'
        verbose_name_plural = '美食'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
