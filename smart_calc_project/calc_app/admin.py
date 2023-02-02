from django.contrib import admin
from .models  import (
    EquipmentType, 
    Equipment,
    BaseHouseWithWaterAnalysis,
    BaseHouseAnalysisEquimpent,
    BaseHouseWithoutWaterAnalysis,
    BaseHouseNoAnalysisEquipment,
    CountryHouseWithWaterAnalysis,
    CoutryHouseAnalysisEquipment,
    CountryHouseWithoutWaterAnalysis,
    CountryHouseNoAnalysisEquipment,
    FlatHouseWithWaterAnalysis,
    FlatHouseAnalysisEquipment,
    FlatHouseWithoutWaterAnalysis,
    FlatHouseNoAnalysisEquipment
)


class MyAdmin(admin.ModelAdmin):
    pass

admin.site.register(EquipmentType, MyAdmin)
admin.site.register(Equipment)

admin.site.register(BaseHouseWithWaterAnalysis)
admin.site.register(BaseHouseAnalysisEquimpent)
admin.site.register(BaseHouseWithoutWaterAnalysis)
admin.site.register(BaseHouseNoAnalysisEquipment)
admin.site.register(CountryHouseWithWaterAnalysis)
admin.site.register(CoutryHouseAnalysisEquipment)
admin.site.register(CountryHouseWithoutWaterAnalysis)
admin.site.register(CountryHouseNoAnalysisEquipment)
admin.site.register(FlatHouseWithWaterAnalysis)
admin.site.register(FlatHouseAnalysisEquipment)
admin.site.register(FlatHouseWithoutWaterAnalysis)
admin.site.register(FlatHouseNoAnalysisEquipment)
