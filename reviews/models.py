from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from foods.models import Food


class Review(models.Model):
    """使用者對美食的評論與評分(評分範圍 1.0 ~ 5.0)"""

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='美食',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='使用者',
    )
    rating = models.DecimalField(
        '評分',
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('1.0')),
            MaxValueValidator(Decimal('5.0')),
        ],
    )
    content = models.TextField('評論內容')
    created_at = models.DateTimeField('建立時間', auto_now_add=True)

    class Meta:
        verbose_name = '評論'
        verbose_name_plural = '評論'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} 對 {self.food} 的評論({self.rating} 星)'
