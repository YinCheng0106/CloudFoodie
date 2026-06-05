from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """註冊表單:在 Django 內建 UserCreationForm 上加入 email 欄位。

    UserCreationForm 已內建密碼強度驗證與「密碼/確認密碼」一致性檢查。
    """

    email = forms.EmailField(label='電子郵件', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 為所有欄位套上 Bootstrap 樣式
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # 將 Django 內建的英文 label / 說明改為繁體中文(T035)
        self.fields['username'].label = '使用者名稱'
        self.fields['username'].help_text = (
            '必填。150 個字元以內,僅可使用英文字母、數字與 @ . + - _ 等符號。'
        )
        self.fields['password1'].label = '密碼'
        self.fields['password1'].help_text = (
            '至少 8 個字元,不可與個人資料太相似,且不能是常見密碼或純數字。'
        )
        self.fields['password2'].label = '確認密碼'
        self.fields['password2'].help_text = '請再次輸入相同的密碼以供確認。'


class LoginForm(AuthenticationForm):
    """登入表單:沿用 Django 內建驗證邏輯,僅套上 Bootstrap 樣式。"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # 繁體中文化欄位標籤(T035)
        self.fields['username'].label = '使用者名稱'
        self.fields['password'].label = '密碼'
