from django.db import models


class UserDemographicsDimension(models.Model):
    user_demographics_id = models.IntegerField(primary_key=True)
    age_group = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50)


class UserDimension(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField()
    phone_credit = models.DecimalField(max_digits=10, decimal_places=2)
    is_admin = models.BooleanField()
    user_demographics = models.ForeignKey(
        UserDemographicsDimension, on_delete=models.CASCADE
    )


class ServiceCategoryDimension(models.Model):
    service_category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=50)


class ServiceDimension(models.Model):
    service_id = models.IntegerField(primary_key=True)
    service_type = models.CharField(max_length=50)
    service_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    service_category = models.ForeignKey(
        ServiceCategoryDimension, on_delete=models.CASCADE
    )


class CharityCategoryDimension(models.Model):
    charity_category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=50)


class CharityDimension(models.Model):
    charity_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    charity_category = models.ForeignKey(
        CharityCategoryDimension, on_delete=models.CASCADE
    )


class DateDimension(models.Model):
    date_id = models.IntegerField(primary_key=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    day_of_week = models.CharField(max_length=10)


class TransactionTypeDimension(models.Model):
    transaction_type_id = models.IntegerField(primary_key=True)
    transaction_type = models.CharField(max_length=50)


class TransactionFact(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(UserDimension, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceDimension, on_delete=models.CASCADE, null=True, blank=True)
    charity = models.ForeignKey(CharityDimension, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.ForeignKey(TransactionTypeDimension, on_delete=models.CASCADE)
    date = models.ForeignKey(DateDimension, on_delete=models.CASCADE)
  
