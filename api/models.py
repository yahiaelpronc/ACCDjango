from django.db import models
from datetime import datetime
# Create your models here.


class Myuser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=30, null=False)
    firstname = models.CharField(max_length=30, null=False)
    lastname = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, max_length=30, null=False)
    password = models.CharField(max_length=30, null=False)
    country = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=20, null=True)
    b_date = models.DateField(max_length=20, null=True)
    active_status = models.BooleanField(default=False)
    face_link = models.URLField(null=True)
    active_link = models.URLField(null=True)
    profile_pic = models.ImageField(null=True)


class Vet(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=30, null=False)
    firstname = models.CharField(max_length=30, null=False)
    lastname = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, max_length=30, null=False)
    password = models.CharField(max_length=30, null=False)
    country = models.CharField(max_length=30, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    b_date = models.DateField(max_length=20, null=True, blank=True)
    active_status = models.BooleanField(default=False)
    face_link = models.URLField(null=True, blank=True)
    active_link = models.URLField(null=True, blank=True)
    profile_pic = models.ImageField(null=False)
    address = models.CharField(max_length=40, null=False)
    specialization = models.CharField(max_length=100, null=False, choices=(('poultry', 'poultry'), ('equine', 'equine'), ('ruminant', 'ruminant'),
                                                                           ('fishes and aquatics',
                                                                            'fishes and aquatics'),
                                                                           ('obstetrics and gynecology', 'obstetrics and gynecology')))


class locations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30, null=False)
    email = models.EmailField(unique=True, max_length=30, null=False)
    address = models.CharField(max_length=40, null=False)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    picture = models.ImageField(null=True, blank=True)
    work_hours_start = models.IntegerField(null=False)
    work_hours_start_period = models.CharField(
        max_length=2, null=False, choices=(('am', 'am'), ('pm', 'pm')))
    work_hours_end = models.IntegerField(null=False)
    work_hours_end_period = models.CharField(
        max_length=2, null=False, choices=(('am', 'am'), ('pm', 'pm')))


class Messages(models.Model):
    content = models.CharField(max_length=300, null=False)
    sender = models.CharField(max_length=30, null=False)
    receiver = models.CharField(max_length=30, null=False)
    date = models.CharField(
        max_length=30, default=str(datetime.now().date()))


class Animal(models.Model):
    animalName = models.CharField(unique=True, max_length=30, null=False)
    ownerUsername = models.CharField(max_length=30, null=False)
    weight = models.IntegerField(null=False)
    b_date = models.DateField(max_length=20, null=False)
    picture = models.ImageField(null=True, blank=True)
    gender = models.CharField(
        max_length=30, null=False, choices=(('m', 'm'), ('f', 'f')))
    species = models.CharField(
        max_length=30, null=False, choices=(('cat', 'cat'), ('dog', 'dog'), ('cow', 'cow')))
    female_state = models.CharField(
        max_length=30, null=True, blank=True, choices=(
            ('immature', 'immature'), ('mature&married', 'mature&married'), ('pregnant ', 'pregnant'), ('lactating', 'lactating')))
