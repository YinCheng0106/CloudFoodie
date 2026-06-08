from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    email = forms.EmailField(label='電子郵件', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['username'].label = '使用者名稱'
        self.fields['password'].label = '密碼'
