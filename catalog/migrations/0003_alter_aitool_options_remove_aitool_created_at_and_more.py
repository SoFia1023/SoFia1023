# Generated by Django 5.1.7 on 2025-03-09 20:06

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_aitool_options_aitool_created_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aitool',
            options={},
        ),
        migrations.RemoveField(
            model_name='aitool',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='aitool',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='aitool',
            name='api_endpoint',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='aitool',
            name='api_model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='aitool',
            name='api_type',
            field=models.CharField(choices=[('openai', 'OpenAI API'), ('huggingface', 'Hugging Face API'), ('custom', 'Custom Integration'), ('none', 'No Integration')], default='none', max_length=50),
        ),
        migrations.AddField(
            model_name='aitool',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='aitool',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='aitool',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='aitool',
            name='endpoint',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='aitool',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='aitool',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ai_images/'),
        ),
        migrations.AlterField(
            model_name='aitool',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='aitool',
            name='popularity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='aitool',
            name='provider',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='New Conversation', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ai_tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.aitool')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('is_user', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.conversation')),
            ],
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ai_tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.aitool')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'ai_tool')},
            },
        ),
    ]
