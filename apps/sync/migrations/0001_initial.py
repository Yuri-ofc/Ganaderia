import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farms', '0001_initial'),
        ('measurements', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SyncChange',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('resource', models.CharField(max_length=100)),
                ('object_id', models.UUIDField()),
                ('action', models.CharField(choices=[('create', 'Crear'), ('update', 'Actualizar'), ('delete', 'Eliminar')], max_length=10)),
                ('payload', models.JSONField(default=dict)),
                ('synchronized_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sync_changes', to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sync_changes', to='measurements.device')),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sync_changes', to='farms.farm')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('device', 'resource', 'object_id', 'action', 'created_at'), name='unique_sync_change')],
            },
        ),
    ]
