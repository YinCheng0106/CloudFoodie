from django import forms

from .models import Food


class FoodForm(forms.ModelForm):
    """新增 / 編輯美食表單。座標 latitude/longitude 為選填,用於詳細頁顯示 Google 地圖。"""

    class Meta:
        model = Food
        fields = ['title', 'category', 'address', 'note', 'image', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例如:超強拉麵屋'}),
            'address': forms.TextInput(attrs={'placeholder': '例如:台北市大安區復興南路一段100號'}),
            'note': forms.Textarea(attrs={'rows': 4, 'placeholder': '寫下你的用餐心得、推薦菜色…'}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': '選填,留空即可'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': '選填,留空即可'}),
        }
        help_texts = {
            'address': '建議填寫完整地址(含路名、門牌),地圖會依此自動定位,避免只填店名造成分店誤判。',
            'latitude': '進階選填。通常留空即可,系統會用上方地址自動定位;若地址定位不準,再填精確緯度覆蓋。',
            'longitude': '進階選填。需與緯度一起填寫,用於精確定位。',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 套上 Bootstrap 樣式:下拉選單用 form-select,其餘用 form-control
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-select' if name == 'category' else 'form-control'
