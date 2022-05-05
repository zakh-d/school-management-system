from django.test import TestCase, Client
from django.urls import reverse, resolve

from school.views import ClassCreateView


class ClassCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.create_url = reverse('school:class_create')
        self.response = self.client.get(self.create_url)

    def test_class_create_view(self):
        view = resolve(self.create_url).func.view_class
        self.assertEqual(view.__name__, ClassCreateView.__name__)

    def test_class_create_template(self):
        # self.assertTemplateUsed(self.response, 'class/create.html')
        print(self.response)
