from django import forms

from .models import Review

# 評分選項:1.0 ~ 5.0(每 0.5 一級),以星號標示方便使用者選擇
RATING_CHOICES = [
    ('5.0', '5.0 ★★★★★'),
    ('4.5', '4.5 ★★★★☆'),
    ('4.0', '4.0 ★★★★'),
    ('3.5', '3.5 ★★★☆'),
    ('3.0', '3.0 ★★★'),
    ('2.5', '2.5 ★★☆'),
    ('2.0', '2.0 ★★'),
    ('1.5', '1.5 ★☆'),
    ('1.0', '1.0 ★'),
]


class ReviewForm(forms.ModelForm):
    """評論表單(T018):提供評分與評論內容兩個欄位。"""

    class Meta:
        model = Review
        fields = ['rating', 'content']
        labels = {
            'rating': '評分',
            'content': '評論內容',
        }
        widgets = {
            'rating': forms.Select(
                choices=RATING_CHOICES,
                attrs={'class': 'form-select'},
            ),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '分享你的用餐體驗、推薦菜色或注意事項…',
            }),
        }
