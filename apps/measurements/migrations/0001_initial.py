import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cattle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AIModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('version', models.CharField(max_length=100, unique=True)),
                ('calibration', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('unit', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('model_name', models.CharField(max_length=100)),
                ('operating_system', models.CharField(max_length=100)),
                ('last_connected_at', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('captured_at', models.DateTimeField()),
                ('capture_mode', models.CharField(choices=[('video', 'Video'), ('photo', 'Foto')], max_length=10)),
                ('estimated_weight_kg', models.DecimalField(decimal_places=2, max_digits=6)),
                ('confidence_interval_min_kg', models.DecimalField(decimal_places=2, max_digits=6)),
                ('confidence_interval_max_kg', models.DecimalField(decimal_places=2, max_digits=6)),
                ('body_condition_score', models.DecimalField(decimal_places=1, max_digits=3)),
                ('confidence_level', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ai_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='measurements', to='measurements.aimodel')),
                ('cattle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='measurements', to='cattle.cattle')),
                ('corrects', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='corrections', to='measurements.measurement')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='measurements', to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='measurements', to='measurements.device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScaleWeighing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('weighed_at', models.DateTimeField()),
                ('scale_type', models.CharField(max_length=100)),
                ('actual_weight_kg', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cattle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scale_weighings', to='cattle.cattle')),
                ('corrects', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='corrections', to='measurements.scaleweighing')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scale_weighings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MorphometricMeasurement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('measurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='morphometrics', to='measurements.measurement')),
                ('measurement_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='records', to='measurements.measurementtype')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('measurement', 'measurement_type'), name='unique_morphometric_measurement_type')],
            },
        ),
    ]
