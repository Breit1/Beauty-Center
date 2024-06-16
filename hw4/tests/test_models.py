from django.core.exceptions import ValidationError
from django.test import TestCase
from buty_center.models import Address, Center, Service, Comments, CenterService
from django.contrib.auth import get_user_model


def create_test(data_change):
    def new_test(self):
        data = self._creation_attrs.copy()
        for attr, value in data_change.items():
            data[attr] = value
        instance = self._model_class(**data)
        with self.assertRaises(ValidationError):
            instance.full_clean()
            instance.save()

    return new_test


def create_test_save(data_change):
    def new_test(self):
        data = self._creation_attrs.copy()
        instance = self._model_class.objects.create(**data)
        for attr, value in data_change.items():
            setattr(instance, attr, value)
        with self.assertRaises(ValidationError):
            instance.full_clean()
            instance.save()

    return new_test


def create_model_test(model_class, creation_attrs, tests):
    class ModelTest(TestCase):
        _model_class = model_class
        _creation_attrs = creation_attrs

        def test_successful_creation(self):
            instance = self._model_class(**self._creation_attrs)
            instance.full_clean()
            instance.save()

    underscore = "_"
    for num, test in enumerate(tests):
        test_name_parts = []
        change_fields = {}
        for attr, value in test:
            change_fields[attr] = value
            test_name_parts.append(attr)
        test_name = underscore.join(test_name_parts)
        setattr(ModelTest, f"test_create_{test_name}_{num}", create_test(change_fields))
        setattr(
            ModelTest, f"test_save_{test_name}_{num}", create_test_save(change_fields)
        )


address_attrs = {
    "street": "Main St",
    "city": "Anytown",
    "state": "State",
    "number": 123,
}

center_attrs = {
    "name": "Main Center",
    "phone": "+71234567890",
}

service_attrs = {
    "name": "Main Service",
    "category": "Category",
}

comment_attrs = {
    "content": "Great service!",
    "mark": 4.5,
}

center_service_attrs = {
    "description": "Service description",
}

address_tests = (
    (("number", -1),),
    (("state", None),),
    (("state", ""),),
    (("state", 123),),
)

center_tests = (
    (("phone", "1234567890"),),
    (("phone", "+71234567890123"),),
)

comment_tests = (
    (("mark", 0),),
    (("mark", 6),),
)


create_model_test(Address, address_attrs, address_tests)
create_model_test(Center, center_attrs, center_tests)
create_model_test(Comments, comment_attrs, comment_tests)

"""Unit tests for the CenterService model."""


class CenterServiceModelTest(TestCase):

    _model_class = CenterService

    def setUp(self):
        self.address = Address.objects.create(**address_attrs)
        self.center = Center.objects.create(**center_attrs, address=self.address)
        self.service = Service.objects.create(**service_attrs)
        self.center_service_attrs = {
            "center": self.center,
            "service": self.service,
            "description": "Service description",
        }

    def test_successful_creation(self):
        instance = self._model_class(**self.center_service_attrs)
        instance.full_clean()
        instance.save()

    def test_invalid_center(self):
        self.center_service_attrs["center"] = None
        instance = self._model_class(**self.center_service_attrs)
        with self.assertRaises(ValidationError):
            instance.full_clean()

    def test_invalid_service(self):
        self.center_service_attrs["service"] = None
        instance = self._model_class(**self.center_service_attrs)
        with self.assertRaises(ValidationError):
            instance.full_clean()


class ServiceModelTest(TestCase):

    _model_class = Service

    def setUp(self):
        self.service_attrs = {
            "name": "Main Service",
            "category": "Category",
        }

    def test_successful_creation(self):
        instance = self._model_class(**self.service_attrs)
        instance.full_clean()
        instance.save()

    def test_invalid_name(self):
        self.service_attrs["name"] = ""
        instance = self._model_class(**self.service_attrs)
        with self.assertRaises(ValidationError):
            instance.full_clean()

    def test_invalid_category(self):
        self.service_attrs["category"] = ""
        instance = self._model_class(**self.service_attrs)
        with self.assertRaises(ValidationError):
            instance.full_clean()


class AddressModelTest(TestCase):

    _model_class = Address

    def setUp(self):
        self.address_attrs = {
            "street": "Main St",
            "city": "Anytown",
            "state": "State",
            "number": 123,
        }

    def test_clean_negative_number(self):
        """Test clean method for Address model with negative number."""
        self.address_attrs["number"] = -1
        instance = self._model_class(**self.address_attrs)
        with self.assertRaises(ValidationError) as cm:
            instance.clean()
        self.assertEqual(str(cm.exception), "['Number cannot be negative.']")

    def test_str_representation(self):
        """Test __str__ method for Address model."""
        instance = self._model_class(**self.address_attrs)
        self.assertEqual(str(instance), "Main St, Anytown, State, 123")


class CenterModelTest(TestCase):

    _model_class = Center

    def setUp(self):
        self.address = Address.objects.create(**address_attrs)
        self.center_attrs = {
            "name": "Main Center",
            "phone": "+71234567890",
            "address": self.address,
        }

    def test_clean_invalid_phone_format(self):
        """Test clean method for Center model with invalid phone number format."""
        self.center_attrs["phone"] = "1234567890"
        instance = self._model_class(**self.center_attrs)
        with self.assertRaises(ValidationError) as cm:
            instance.clean()
        self.assertEqual(str(cm.exception), "['Invalid Russian phone number format.']")

    def test_str_representation(self):
        """Test __str__ method for Center model."""
        instance = self._model_class.objects.create(**self.center_attrs)
        expected_str = f"Center object ({instance.pk})"
        self.assertEqual(str(instance), expected_str)


class CommentsModelTest(TestCase):

    _model_class = Comments

    def setUp(self):
        self.comment_attrs = {
            "content": "Great service!",
            "mark": 4.5,
        }
        self.address = Address.objects.create(**address_attrs)
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )
        self.center = Center.objects.create(
            name="Test Center", phone="+71234567890", address=self.address
        )

    def test_clean_invalid_mark(self):
        comment = Comments(**comment_attrs, center=self.center, user=self.user)
        comment.mark = 0
        with self.assertRaises(ValidationError) as cm:
            comment.clean()
        self.assertEqual(str(cm.exception), "['Mark must be between 1 and 5.']")

    def create_center(self):
        return Center.objects.create(name="Test Center", phone="+71234567890")

    def test_str_representation(self):
        """Test __str__ method for Comments model."""
        instance = self._model_class.objects.create(
            **self.comment_attrs, center=self.center, user=self.user
        )
        expected_str = f"{instance.content}, {instance.mark}, {self.center}"
        self.assertEqual(str(instance), expected_str)
