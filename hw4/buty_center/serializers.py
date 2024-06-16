from rest_framework import serializers
from .models import Address, Center, Service, Comments, CenterService
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class CenterServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = CenterService
        fields = "__all__"


class CenterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    services = serializers.SerializerMethodField()

    class Meta:
        model = Center
        fields = "__all__"

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        center = Center.objects.create(address=address, **validated_data)
        return center

    def get_services(self, obj):
        center_services = CenterService.objects.filter(center=obj)
        return CenterServiceSerializer(center_services, many=True).data

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)
        if address_data:
            address_instance = instance.address
            for attr, value in address_data.items():
                setattr(address_instance, attr, value)
            address_instance.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    center_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Comments
        fields = ["id", "content", "mark", "center_id", "user", "created_at"]
        read_only_fields = ["user", "created_at", "center"]

    def create(self, validated_data):
        center_id = validated_data.pop("center_id", None)
        if not center_id:
            raise ValidationError("Center ID is required.")

        try:
            center = Center.objects.get(pk=center_id)
        except Center.DoesNotExist:
            raise ValidationError("Invalid Center ID.")

        user = self.context["request"].user
        comment = Comments.objects.create(center=center, user=user, **validated_data)
        return comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
