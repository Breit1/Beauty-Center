from django.contrib import admin
from .models import Center, Service, Comments, CenterService, Address


class CenterAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone")
    search_fields = (
        "name",
        "address__street",
        "phone",
        "address__city",
        "address__state",
    )


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name", "category")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("content", "mark", "center", "user")
    search_fields = (
        "content",
        "center__name",
        "center__address__street",
        "center__address__city",
        "center__address__state",
    )
    list_filter = ("mark",)


class CenterServiceAdmin(admin.ModelAdmin):
    list_display = ("center", "service", "description")
    search_fields = ("center__name", "service__name", "description")
    list_filter = ("center", "service")


class AddressAdmin(admin.ModelAdmin):
    list_display = ("street", "city", "state", "number")
    search_fields = ("street", "city", "state", "number")


admin.site.register(Center, CenterAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(CenterService, CenterServiceAdmin)
admin.site.register(Address, AddressAdmin)
