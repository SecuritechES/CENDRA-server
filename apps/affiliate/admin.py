from django.contrib import admin
from .models import Affiliate, PaymentChoice

class AffiliateAdmin(admin.ModelAdmin):
    list_filter = ("entity",)
    list_display = ("entity", "show_fullname")

    def show_fullname(self, obj):
        return obj.name + " " + obj.surnames
    
    show_fullname.short_description = "Nombre"


class PaymentChoiceAdmin(admin.ModelAdmin):
    list_filter = ("affiliate__entity",)
    list_display = ("show_entity", "show_fullname", "show_payment_choice")

    def show_entity(self, obj):
        return obj.affiliate.entity
    
    def show_fullname(self, obj):
        return obj.affiliate.name + " " + obj.affiliate.surnames
    
    def show_payment_choice(self, obj):
        return obj.affiliate.get_payment_choice_display
    
    show_entity.short_description = "Asociación"
    show_fullname.short_description = "Nombre"
    show_payment_choice.short_description = "Forma de pago"

admin.site.register(Affiliate, AffiliateAdmin)
    
admin.site.register(PaymentChoice, PaymentChoiceAdmin)
