from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from buty_center.models import Address, Center, Service, Comments, CenterService
from django.contrib.auth.models import User


class AddressAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", password="password", email="test@example.com"
        )
        self.address = Address.objects.create(
            street="Main St", city="Anytown", state="State", number=123
        )

    def test_get_address_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("address-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_address(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("address-list")
        data = {
            "street": "New St",
            "city": "Newtown",
            "state": "New State",
            "number": 456,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 2)

    def test_get_address_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("address-detail", args=[self.address.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["street"], "Main St")

    def test_update_address(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("address-detail", args=[self.address.id])
        data = {
            "street": "Updated St",
            "city": "Anytown",
            "state": "State",
            "number": 123,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Address.objects.get(id=self.address.id).street, "Updated St")

    def test_delete_address(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("address-detail", args=[self.address.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Address.objects.count(), 0)


class CenterAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", password="password", email="test@example.com"
        )
        self.address = Address.objects.create(
            street="Main St", city="Anytown", state="State", number=123
        )
        self.center = Center.objects.create(
            name="Main Center", phone="+71234567890", address=self.address
        )

    def test_get_center_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("center-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_center(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("center-list")
        address = Address.objects.create(
            street="Новая улица", city="Новый город", state="Новый штат", number=456
        )
        data = {
            "name": "Новый Центр",
            "phone": "+71234567891",
            "address": {
                "id": address.id,
                "street": address.street,
                "city": address.city,
                "state": address.state,
                "number": address.number,
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_center_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("center-detail", args=[self.center.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Main Center")

    def test_update_center(self):
        self.client.force_authenticate(user=self.user)

        # Создаем новый адрес для центра
        new_address = Address.objects.create(
            street="Новая улица", city="Новый город", state="Новый штат", number=456
        )

        center = Center.objects.create(
            name="Центр для обновления", phone="+71234567890", address=new_address
        )

        url = reverse("center-detail", args=[center.id])
        updated_data = {
            "name": "Обновленный Центр",
            "phone": "+71234567891",
            "address": {
                "id": new_address.id,
                "street": new_address.street,
                "city": new_address.city,
                "state": new_address.state,
                "number": new_address.number,
            },
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_center(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("center-detail", args=[self.center.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Center.objects.count(), 0)


class ServiceAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", password="password", email="test@example.com"
        )
        self.service = Service.objects.create(name="Service 1")

    def test_get_service_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("service-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_service_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("service-detail", args=[self.service.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Service 1")

    def test_delete_service(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("service-detail", args=[self.service.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Service.objects.count(), 0)


class CommentsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", password="password", email="test@example.com"
        )
        self.address = Address.objects.create(
            street="Main St", city="Anytown", state="State", number=123
        )
        self.center = Center.objects.create(
            name="Main Center", phone="+71234567890", address=self.address
        )
        self.comment = Comments.objects.create(
            content="Great service!", mark=4.5, center=self.center, user=self.user
        )

    def test_get_comment_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("comments-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("comments-detail", args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Great service!")

    def test_update_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("comments-detail", args=[self.comment.id])
        data = {"content": "Updated comment", "mark": 4.0, "center": self.center.id}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Comments.objects.get(id=self.comment.id).content, "Updated comment"
        )

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("comments-detail", args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comments.objects.count(), 0)


class CenterServiceAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", password="password", email="test@example.com"
        )
        self.address = Address.objects.create(
            street="Main St", city="Anytown", state="State", number=123
        )
        self.center = Center.objects.create(
            name="Main Center", phone="+71234567890", address=self.address
        )
        self.service = Service.objects.create(name="Service 1")
        self.center_service = CenterService.objects.create(
            center=self.center, service=self.service
        )

    def test_get_center_service_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("centerservice-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_center_service_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("centerservice-detail", args=[self.center_service.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["center"], self.center.id)

    def test_delete_center_service(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("centerservice-detail", args=[self.center_service.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CenterService.objects.count(), 0)
