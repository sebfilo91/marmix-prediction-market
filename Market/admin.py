from django.contrib import admin
from Market.models import *

class ClaimAdmin(admin.ModelAdmin):
    pass

class TraderAdmin(admin.ModelAdmin):
    pass

class RewardAdmin(admin.ModelAdmin):
    pass

class CurrencyAdmin(admin.ModelAdmin):
    pass

class ExchangeAdmin(admin.ModelAdmin):
    pass

class HelpAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trader,TraderAdmin)
admin.site.register(Claim,ClaimAdmin)
admin.site.register(Reward,RewardAdmin)
admin.site.register(Exchange,ExchangeAdmin)
admin.site.register(Currency,CurrencyAdmin)
admin.site.register(Help,HelpAdmin)