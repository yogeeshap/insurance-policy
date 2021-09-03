from django.db import models

# Create your models here.

class Customer(models.Model):
    
    """
        This model is normaiilzed according to requirement
    """

    CUSTOMER_INCOME_GROUP_CHOICES = (
        (0, "0- $25K"),
        (1, "$25-$70K"),
        (2, ">$70K")
        )
    
    CUSTOMER_REGION_CHOICES = (
        ('North', "North"),
        ('East', "East"),
        ('West', "West"),
        ('South', "South")
        )
    
    CUSTOMER_MARTIAL_STATUS_CHOICES = (
        (0, "Single"),
        (1, "Married"),
        (2, "Other")
        )
    
    CUSTOMER_GENDER_CHOICES = (
        (0, "Male"),
        (1, "Female"),
        (2, "Other")
        )

    customer_digit = models.PositiveIntegerField(default=None)
    customer_income_group = models.IntegerField(choices=CUSTOMER_INCOME_GROUP_CHOICES, default=0)
    customer_region = models.CharField(choices=CUSTOMER_REGION_CHOICES,max_length = 200)
    customer_martial_status = models.IntegerField(choices=CUSTOMER_MARTIAL_STATUS_CHOICES, default=2)
    customer_gender_status = models.IntegerField(choices=CUSTOMER_GENDER_CHOICES, default=2)

    class Meta:
        db_table = 'customer'


class PolicyDetails(models.Model):
    """
        This model is normaiilzed according to requirement
    """

    FUEL_CHOICES = (
        (0, "CNG"),
        (1, "Petrol"),
        (2, "Diesel")
        )

    VEHICLE_SEGMENT_CHOICES = (
        ('A', "Mini Hatchbacks"),
        ('B', "Small Hatchbacks"),
        ('C', "Small Sedans or family cars"),
        ('D', "Mid-Sized Family cars or Sedans"),
        ('E', "SExecutive Luxury Cars"),
        ('F', "MPVs"),
        ('G', "SUVs"),
        )

    policy_id =  models.CharField(max_length = 200)
    date_of_purchase = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='policy_details',default=None)
    fuel = models.IntegerField(choices=FUEL_CHOICES)   
    vehicle_segment = models.CharField(choices=VEHICLE_SEGMENT_CHOICES,max_length = 200)
    premium = models.PositiveIntegerField(blank=True,null=True)   
    bodily_injury_liability = models.PositiveIntegerField(blank=True,null=True)
    personal_injury_liability = models.PositiveIntegerField(blank=True,null=True)
    property_damage_liability = models.PositiveIntegerField(blank=True,null=True)
    colision = models.PositiveIntegerField(blank=True,null=True)
    comprehensive = models.PositiveIntegerField(blank=True,null=True)

    class Meta:
        db_table = 'policy_details'
