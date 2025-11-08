import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('amount_saved', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('target_date', models.DateField(blank=True, null=True)),
                ('priority', models.CharField(choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')], default='MEDIUM', max_length=10)),
                ('image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='IN_PROGRESS', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
