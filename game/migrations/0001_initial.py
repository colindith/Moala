# Generated by Django 2.1.2 on 2018-12-08 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Undefined'), (1, 'Growing'), (2, 'Ripening'), (3, 'Dead')], default=0)),
                ('ripening_age', models.IntegerField(default=100)),
                ('growing_speed', models.FloatField(default=1.0)),
                ('age', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Plan',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CropSpecies',
            fields=[
                ('name', models.CharField(max_length=40)),
                ('code', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('base_ripening_age', models.IntegerField(default=100)),
                ('base_growing_speed', models.FloatField(default=1.0)),
                ('reward_generator', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CropSpeciesRewardDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=1)),
                ('crop_species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reward_cropses', to='game.CropSpecies')),
                ('item_prototype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.ItemPrototype')),
            ],
        ),
        migrations.AddField(
            model_name='cropspecies',
            name='reward_choices',
            field=models.ManyToManyField(related_name='crop_species', through='game.CropSpeciesRewardDetail', to='item.ItemPrototype'),
        ),
        migrations.AddField(
            model_name='crop',
            name='crop_species',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crops', to='game.CropSpecies'),
        ),
        migrations.AlterUniqueTogether(
            name='cropspeciesrewarddetail',
            unique_together={('crop_species', 'item_prototype')},
        ),
    ]
