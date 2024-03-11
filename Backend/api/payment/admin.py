from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_code', 'transaction_uuid', 'status')
    search_fields = ['user', 'transaction_code', 'transaction_uuid']

admin.site.register(Payment, PaymentAdmin)
