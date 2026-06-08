
import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(Decimal('1.0')), django.core.validators.MaxValueValidator(Decimal('5.0'))], verbose_name='評分')),
                ('content', models.TextField(verbose_name='評論內容')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='foods.food', verbose_name='美食')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            options={
                'verbose_name': '評論',
                'verbose_name_plural': '評論',
                'ordering': ['-created_at'],
            },
        ),
    ]
