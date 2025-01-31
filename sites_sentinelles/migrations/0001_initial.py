# Generated by Django 4.1.13 on 2024-04-27 19:01

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='COUNTRY',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Laboratoire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('Sites_sentinelles', models.CharField(max_length=100)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites_sentinelles.country')),
            ],
        ),
        migrations.CreateModel(
            name='SENTINELLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(blank=True)),
                ('Type_de_Site', models.CharField(choices=[('Hopitalier', 'Hopitalier'), ('Communautaire', 'Communautaire'), ('Laboratoire ', 'Laboratoire')], max_length=25)),
                ('Nombre_IRA_Syndrômme_gripaux', models.CharField(blank=True, max_length=100)),
                ('IRA', models.CharField(blank=True, max_length=100)),
                ('Suspect_COVID', models.CharField(blank=True, max_length=100)),
                ('Hospitalisation', models.CharField(blank=True, max_length=100)),
                ('Cas_Preleves', models.CharField(blank=True, max_length=100)),
                ('Cas_Positif_Covid', models.CharField(blank=True, max_length=100)),
                ('Cas_Positif_Influenza', models.CharField(blank=True, max_length=100)),
                ('Cas_Positif_Autres_virus', models.CharField(blank=True, max_length=100)),
                ('Cas_Positif_RSV', models.CharField(blank=True, max_length=100)),
                ('IRA_Positif_Covid', models.CharField(blank=True, max_length=100)),
                ('Deces_covid', models.CharField(blank=True, max_length=100)),
                ('Deces_IRA_covid', models.CharField(blank=True, max_length=100)),
                ('Sexe', models.CharField(choices=[('HOMME ', 'HOMME'), ('FEMME', 'FEMME')], max_length=15)),
                ('Groupe_age', models.CharField(choices=[('< 5 ans', '< 5 ans'), ('5-15 ans', '5-15 ans'), ('15-50 ans', '15-50 ans'), ('50 ans et plus', '50 ans et plus'), ('Age manquant', 'Age manquant')], max_length=100)),
                ('nombre_de_Consultation', models.CharField(blank=True, max_length=100)),
                ('Statut_Vaccinal', models.CharField(choices=[('Tous', 'Tous'), ('Totalement', 'Totalement'), ('Partiellement ', 'Partiellement '), ('Pas Vacciné', 'Pas Vacciné'), ('Aucun', 'Aucun')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Sites_sentinelles', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites_sentinelles.laboratoire')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites_sentinelles.country')),
            ],
            options={
                'permissions': (('can_view_data_for_country', 'Peut voir les données pour son pays'),),
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('institution', models.CharField(choices=[('Centre Pasteur du Cameroun', 'Centre Pasteur du Cameroun'), ('Institut Pasteur de Bangui (IPB)', 'Institut Pasteur de Bangui (IPB)'), ('Institut Pasteur de Dakar (IPD)', 'Institut Pasteur de Dakar (IPD)'), ('Institut Pasteur de Madagascar (IPM)', 'Institut Pasteur de Madagascar (IPM)'), ('Institut de Recherche Clinique du Bénin (IRCB)', 'Institut de Recherche Clinique du Bénin (IRCB)'), ('Institut Pasteur de Côte  Ivoire', 'Institut Pasteur de Côte  Ivoire'), ('Institut Pasteur de Guinée', 'Institut Pasteur de Guinée'), ('Institut commémoratif Noguchi pour la recherche médicale  Accra (NMIMR)', 'Institut commémoratif Noguchi pour la recherche médicale Accra (NMIMR)'), ('Institut National de Santé Publique Ouagadougou (INSP)', 'Institut National de Santé Publique Ouagadougou (INSP)'), ('CERMES Niamey ', 'CERMES Niamey'), ('Institut National de Santé Publique Bamako (INSP)', 'Institut National de Santé Publique Bamako (INSP)'), ('Institut National de Recherche Biomédicale Kinshasa (INRB)', 'Institut National de Recherche Biomédicale Kinshasa (INRB)'), ('Laboratoire de Biologie Moléculaire et d’Immunologie Lomé (BIOLIM)', 'Laboratoire de Biologie Moléculaire et d’Immunologie Lomé (BIOLIM)')], max_length=200)),
                ('statut', models.CharField(blank=True, choices=[('Activated', 'Activated'), ('Deactivated', 'Deactivated'), ('Rejected', 'Rejected'), ('Pending Approval', 'Pending Approval')], default='Deactivated', max_length=20)),
                ('token_expiration_date', models.DateTimeField(blank=True, null=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites_sentinelles.country')),
                ('groups', models.ManyToManyField(related_name='sites_sentinelles_users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
