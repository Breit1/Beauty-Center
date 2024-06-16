from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Address(UUIDMixin):
    street = models.TextField(_("street"), null=False, blank=False)
    city = models.TextField(_("city"), null=False, blank=False)
    state = models.TextField(_("state"), null=False, blank=False)
    number = models.IntegerField(_("number"), null=False, blank=False)

    class Meta:
        db_table = "api_data_address"
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.state}, {self.number}"

    def clean(self):
        super().clean()
        if self.number < 0:
            raise ValidationError(_("Number cannot be negative."))


class Center(UUIDMixin):
    name = models.TextField(_("name"), null=False, blank=False)
    address = models.OneToOneField(
        "Address", verbose_name=_("address"), on_delete=models.CASCADE
    )
    phone = models.CharField(_("phone number"), max_length=15, null=False, blank=False)

    def clean(self):
        super().clean()
        if not re.match(r"^((\+7|7|8)+([0-9]){10})$", self.phone):
            raise ValidationError(_("Invalid Russian phone number format."))

    class Meta:
        db_table = "api_data_center"
        ordering = ["name"]
        verbose_name = _("center")
        verbose_name_plural = _("centers")


class Service(UUIDMixin):
    name = models.TextField(_("name"), null=False, blank=False)
    category = models.TextField(_("category"), null=False, blank=False)
    centers = models.ManyToManyField(
        "Center", verbose_name=_("centers"), through="CenterService"
    )

    class Meta:
        db_table = "api_data_service"
        ordering = ["name"]
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self) -> str:
        return f"{self.name}, {self.category}, {self.centers}"


class Comments(UUIDMixin):
    content = models.TextField(_("content"), null=False, blank=False)
    mark = models.FloatField(_("mark"), null=False, blank=False)
    center = models.ForeignKey(
        "Center", verbose_name=_("center"), on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "api_data_comment"
        ordering = ["mark"]
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self) -> str:
        return f"{self.content}, {self.mark}, {self.center}"

    def clean(self):
        super().clean()
        if self.mark < 1 or self.mark > 5:
            raise ValidationError(_("Mark must be between 1 and 5."))


class CenterService(UUIDMixin):
    center = models.ForeignKey(
        "Center", verbose_name=_("center"), on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        "Service", verbose_name=_("service"), on_delete=models.CASCADE
    )
    description = models.TextField(_("description"), null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.center} - {self.service}"

    class Meta:
        db_table = "api_data_center_service"
        verbose_name = _("center_service")
        verbose_name_plural = _("center_services")
