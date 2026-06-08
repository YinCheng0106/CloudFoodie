
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='美食名稱')),
                ('category', models.CharField(choices=[('chinese', '中式'), ('japanese', '日式'), ('korean', '韓式'), ('western', '西式'), ('dessert', '甜點'), ('drink', '飲料'), ('other', '其他')], default='other', max_length=20, verbose_name='分類')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='地址')),
                ('note', models.TextField(blank=True, verbose_name='個人筆記')),
                ('image', models.ImageField(blank=True, null=True, upload_to='foods/', verbose_name='照片')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='緯度')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='經度')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foods', to=settings.AUTH_USER_MODEL, verbose_name='建立者')),
            ],
            options={
                'verbose_name': '美食',
                'verbose_name_plural': '美食',
                'ordering': ['-created_at'],
            },
        ),
    ]
