from django.contrib import admin
from pasarela.models import Provider, Transaction
# Register your models here.

@admin.register(Provider)

class ProviderAdmin(admin.ModelAdmin):
    list_display=['name', 'environment', 'active']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=['amount', 'currency', 'payment_state', 'id_proveedor']