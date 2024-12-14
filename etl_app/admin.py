from django.contrib import admin
from .models import (
    UserDemographicsDimension,
    UserDimension,
    ServiceCategoryDimension,
    ServiceDimension,
    CharityCategoryDimension,
    CharityDimension,
    DateDimension,
    TransactionTypeDimension,
    TransactionFact,
)

# Base Admin Class to Add Custom Buttons
class CustomButtonAdmin(admin.ModelAdmin):
    change_list_template = "charts/custom_change_list.html"

# Custom Admin for UserDemographicsDimension
@admin.register(UserDemographicsDimension)
class UserDemographicsDimensionAdmin(CustomButtonAdmin):
    list_display = ("user_demographics_id", "age_group", "city", "region")
    search_fields = ("age_group", "city", "region")
    list_filter = ("region", "city", "age_group")

# Custom Admin for UserDimension
@admin.register(UserDimension)
class UserDimensionAdmin(CustomButtonAdmin):
    list_display = ("user_id", "username", "phone", "is_active", "phone_credit", "is_admin")
    search_fields = ("username", "phone")
    list_filter = ("is_active", "is_admin", "phone_credit")

# Custom Admin for ServiceCategoryDimension
@admin.register(ServiceCategoryDimension)
class ServiceCategoryDimensionAdmin(CustomButtonAdmin):
    list_display = ("service_category_id", "category_name")
    search_fields = ("category_name",)
    list_filter = ("category_name",)

# Custom Admin for ServiceDimension
@admin.register(ServiceDimension)
class ServiceDimensionAdmin(CustomButtonAdmin):
    list_display = ("service_id", "service_type", "service_number", "amount", "service_category")
    search_fields = ("service_type", "service_number")
    list_filter = ("service_type", "service_category")

# Custom Admin for CharityCategoryDimension
@admin.register(CharityCategoryDimension)
class CharityCategoryDimensionAdmin(CustomButtonAdmin):
    list_display = ("charity_category_id", "category_name")
    search_fields = ("category_name",)
    list_filter = ("category_name",)

# Custom Admin for CharityDimension
@admin.register(CharityDimension)
class CharityDimensionAdmin(CustomButtonAdmin):
    list_display = ("charity_id", "name", "phone_number", "amount", "charity_category")
    search_fields = ("name", "phone_number")
    list_filter = ("charity_category", "name")

# Custom Admin for DateDimension
@admin.register(DateDimension)
class DateDimensionAdmin(CustomButtonAdmin):
    list_display = ("date_id", "day", "month", "year", "day_of_week")
    search_fields = ("year", "month", "day_of_week")
    list_filter = ("year", "month", "day_of_week", "day")

# Custom Admin for TransactionTypeDimension
@admin.register(TransactionTypeDimension)
class TransactionTypeDimensionAdmin(CustomButtonAdmin):
    list_display = ("transaction_type_id", "transaction_type")
    search_fields = ("transaction_type",)
    list_filter = ("transaction_type",)

# Custom Admin for TransactionFact
@admin.register(TransactionFact)
class TransactionFactAdmin(CustomButtonAdmin):
    list_display = (
        "transaction_id",
        "user",
        "service",
        "charity",
        "amount",
        "transaction_type",
        "date",
    )
    search_fields = ("transaction_id", "user__username", "service__service_type", "charity__name")
    list_filter = (
        "transaction_type",
        "date__year",
        "date__month",
        "date__day_of_week",
        "service__service_type",
    )
