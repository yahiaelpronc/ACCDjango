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
    governorate = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=40, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True)
    b_date = models.CharField(max_length=20, null=False)
    active_status = models.BooleanField(default=False)
    face_link = models.CharField(max_length=100, null=True, blank=True)
    active_link = models.URLField(null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    isOnline = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    isOwner = models.BooleanField(default=False)


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
    face_link = models.CharField(max_length=100, null=True, blank=True)
    active_link = models.URLField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    address = models.CharField(max_length=40, null=False)
    specialization = models.CharField(max_length=100, null=False, choices=(('poultry', 'poultry'), ('equine', 'equine'), ('ruminant', 'ruminant'),
                                                                           ('fishes and aquatics',
                                                                            'fishes and aquatics'),
                                                                           ('obstetrics and gynecology', 'obstetrics and gynecology')))
    isOnline = models.BooleanField(default=False)
    isOwner = models.BooleanField(default=False)


class locations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30, null=False)
    owner = models.CharField(unique=False, max_length=30, null=False)
    email = models.EmailField(unique=True, max_length=30, null=False)
    address = models.CharField(max_length=40, null=False)
    governorate = models.CharField(max_length=40, null=False)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    service = models.CharField(
        max_length=30, null=False, choices=(('Wellness Exams & Vaccinations', 'Wellness Exams & Vaccinations'),
                                            ('Boarding & Grooming Services',
                                             'Boarding & Grooming Services'),
                                            ('Animal Emergency Services',
                                             'Animal Emergency Services')
                                            ))
    description = models.CharField(max_length=200, null=True, blank=True)
    website_link = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(null=True, blank=True)
    price = models.IntegerField(null=False, default=0)
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
        max_length=30, null=False, choices=(('male', 'male'), ('female', 'female')))
    species = models.CharField(
        max_length=30, null=False, choices=(('cat', 'cat'), ('dog', 'dog'), ('cow', 'cow')))
    female_state = models.CharField(
        max_length=30, null=True, blank=True, choices=(
            ('immature', 'immature'), ('mature&married', 'mature&married'), ('pregnant ', 'pregnant'), ('lactating', 'lactating')))


class Medication(models.Model):
    animalName = models.CharField(max_length=30, null=False)
    vetName = models.CharField(max_length=30, null=False)
    medicationName = models.CharField(max_length=30, null=False)
    dosage = models.IntegerField(null=False)
    dosageInterval = models.IntegerField(null=False)
    adminstrationRoute = models.CharField(max_length=30, null=True, blank=True, choices=(
        ('Intramascular', 'Intramascular'), ('Intravenous', 'Intravenous'), ('Oral', 'Oral'), ('Sublingual', 'Sublingual'), ('Topical', 'Topical'), ('Ocular', 'Ocular'), ('Subcutaneous', 'Subcutaneous')))
    date = models.CharField(null=True, blank=True,
                            max_length=30, default=str(datetime.now().date()))


class SurgicalOperationsRequest(models.Model):
    id = models.AutoField(primary_key=True)
    animalName = models.CharField(max_length=30, null=False)
    vetName = models.CharField(max_length=30, null=False)
    message = models.CharField(max_length=300, null=False)
    user = models.CharField(max_length=30, null=False)
    statusUser = models.CharField(max_length=30, null=True, blank=True, default='pending', choices=(
        ('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')))
    statusVet = models.CharField(max_length=30, null=True, blank=True, default='pending', choices=(
        ('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')))


class SurgicalOperations(models.Model):
    animalName = models.CharField(max_length=30, null=True, blank=True)
    owner = models.CharField(max_length=30, null=False)
    vetName = models.CharField(max_length=30, null=False)
    operationName = models.CharField(max_length=30, null=False, default="")
    date = models.CharField(max_length=30, null=False, default="")
    price = models.IntegerField(null=False, default=0)

    message = models.CharField(max_length=300, null=False, default="")
    statusUser = models.CharField(max_length=30, null=True, blank=True, default='pending', choices=(
        ('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')))

    statusVet = models.CharField(max_length=30, null=True, blank=True, default='pending', choices=(
        ('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')))
    reasonUser=models.CharField(max_length=300, null=False, default="")
    reasonVet=models.CharField(max_length=300, null=False, default="")


class ServiseRequest(models.Model):
    locationName = models.CharField(max_length=30, null=True, blank=True)
    serviceName = models.CharField(max_length=30, null=False)
    locationOwner = models.CharField(max_length=30, null=False)
    animalOwner = models.CharField(max_length=30, null=False)
    price = models.IntegerField(null=False)
    date = models.CharField(max_length=30, null=False)
    time = models.IntegerField(null=False)
    timePeriod = models.CharField(
        max_length=2, null=False, choices=(('am', 'am'), ('pm', 'pm')))
    AnimalType = models.CharField(
        max_length=30, null=False, choices=(('cat', 'cat'), ('dog', 'dog'), ('cow', 'cow')))
    statusOwner = models.CharField(max_length=30, null=True, blank=True, default='pending', choices=(
        ('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')))
    statusUser = models.CharField(max_length=30, null=True, blank=True, default='accepted', choices=(
        ('accepted', 'accepted'), ('pending', 'pending'), ('declined', 'declined')))
    reasonUser=models.CharField(max_length=300, null=False, default="")
    reasonVet=models.CharField(max_length=300, null=False, default="")


class Notifications(models.Model):
    receiver = models.CharField(max_length=30, null=False)
    type = models.CharField(
        max_length=30, null=False, choices=(('service', 'service'), ('medication', 'medication'), ('surgery', 'surgery')))
    message = models.CharField(max_length=300, default="")
