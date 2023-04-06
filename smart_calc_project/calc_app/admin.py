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


class BaseHouseAnalysisEquimpentInline(admin.TabularInline):
    model = BaseHouseAnalysisEquimpent
    extra = 1

class BaseHouseNoAnalysisEquipmentInline(admin.TabularInline):
    model = BaseHouseNoAnalysisEquipment
    extra = 1

class CoutryHouseAnalysisEquipmentInline(admin.TabularInline):
    model = CoutryHouseAnalysisEquipment
    extra = 1

class CountryHouseNoAnalysisEquipmentInline(admin.TabularInline):
    model = CountryHouseNoAnalysisEquipment
    extra = 1

class FlatHouseAnalysisEquipmentInline(admin.TabularInline):
    model = FlatHouseAnalysisEquipment
    extra = 1

class FlatHouseNoAnalysisEquipmentInline(admin.TabularInline):
    model = FlatHouseNoAnalysisEquipment
    extra = 1
#====================================================================
class BaseHouseWithWaterAnalysisAdmin(admin.ModelAdmin):
    inlines = (BaseHouseAnalysisEquimpentInline,)

class BaseHouseWithoutWaterAnalysisAdmin(admin.ModelAdmin):
    inlines = (BaseHouseNoAnalysisEquipmentInline,)
    
class CountryHouseWithWaterAnalysisAdmin(admin.ModelAdmin):
    inlines = (CoutryHouseAnalysisEquipmentInline,)        

class CountryHouseWithoutWaterAnalysisAdmin(admin.ModelAdmin):
    inlines = (CountryHouseNoAnalysisEquipmentInline,)

class FlatHouseWithWaterAnalysisAdmin(admin.ModelAdmin):
    inlines = (FlatHouseAnalysisEquipmentInline,)

class FlatHouseWithoutWaterAnalysisAdmin(admin.ModelAdmin):
    inlines = (FlatHouseNoAnalysisEquipmentInline,)

admin.site.register(EquipmentType)
admin.site.register(Equipment)

admin.site.register(BaseHouseWithWaterAnalysis, BaseHouseWithWaterAnalysisAdmin)
admin.site.register(BaseHouseAnalysisEquimpent)
admin.site.register(BaseHouseWithoutWaterAnalysis, BaseHouseWithoutWaterAnalysisAdmin)
admin.site.register(BaseHouseNoAnalysisEquipment)
admin.site.register(CountryHouseWithWaterAnalysis, CountryHouseWithWaterAnalysisAdmin)
admin.site.register(CoutryHouseAnalysisEquipment)
admin.site.register(CountryHouseWithoutWaterAnalysis, CountryHouseWithoutWaterAnalysisAdmin)
admin.site.register(CountryHouseNoAnalysisEquipment)
admin.site.register(FlatHouseWithWaterAnalysis, FlatHouseWithWaterAnalysisAdmin)
admin.site.register(FlatHouseAnalysisEquipment)
admin.site.register(FlatHouseWithoutWaterAnalysis, FlatHouseWithoutWaterAnalysisAdmin)
admin.site.register(FlatHouseNoAnalysisEquipment)
