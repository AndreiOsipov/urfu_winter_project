from django.db import models
from django.db.models.functions import Length

models.CharField.register_lookup(Length)


class Equipment(models.Model):
    equipment_id = models.CharField(primary_key=True, max_length=6)
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.FloatField()
    
    class Meta:
        constraints = [
            models.CheckConstraint(check = models.Q(equipment_id__length=6) & 
            models.Q(equipment_id__regex=r'[A-Z][A-Z][0-9][0-9][0-9][0-9]'),
            name='equipment_id_constraint'),
            models.CheckConstraint(check = models.Q(number__gte=0), name='equipment_number_constraint'),
            models.CheckConstraint(check = models.Q(name__length__gt=0), name='equipment_name_constraint'),
            models.CheckConstraint(check=models.Q(price__gte=0), name='equipment_price_constraint'), 
        ]

class Filler(models.Model):
    filler_id = models.CharField(primary_key=True, max_length=6)
    filler_name = models.CharField(max_length=100)
    filler_v = models.FloatField()

    class Meta:
        constraints = [
            models.CheckConstraint(check = models.Q(filler_id__length=6) & 
            models.Q(filler_id__regex=r'[A-Z][A-Z][0-9][0-9][0-9][0-9]'),
            name='filler_id_constraint'),
            models.CheckConstraint(check = models.Q(filler_name__length__gt=0), name='filler_name_constraint'),
            models.CheckConstraint(check = models.Q(filler_v__gte=0), name='filler_v_constraint'),
        ]