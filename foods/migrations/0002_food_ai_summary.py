
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='ai_summary',
            field=models.TextField(blank=True, verbose_name='AI 摘要'),
        ),
    ]
