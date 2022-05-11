from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
import pandas as pd

from accounts.models import AdministrationMember, Teacher
from school.models import School, Class
from student.forms import StudentExcelUploadForm
from student.models import Student


class StudentModelTests(TestCase):

    def setUp(self):
        school = School.objects.create(name='TEST SCHOOL')
        _class = Class.objects.create(name='10-A', school=school)
        self.student = Student.objects.create(
            first_name='Jack',
            last_name='Sparrow',
            order_in_class=1,
            origin_class=_class
        )

    def test_str(self):
        self.assertEqual(str(self.student), 'Jack Sparrow')


class StudentExcelUploadViewTests(TestCase):

    def setUp(self):
        school = School.objects.create(name='TEST SCHOOL')
        self._class = Class.objects.create(name='10-A', school=school)
        user = AdministrationMember(
            first_name='test',
            last_name='test',
            username='user',
            email='user@mail.com',
            school=school
        )
        user.set_password('testpass123')
        user.save()

    def test_raises_404(self):
        self.client.login(username='user', password='testpass123')
        url = reverse('student:upload', kwargs={'class_id': 'f50e8400-e29b-41d4-a716-446655440000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_redirects_to_login(self):
        url = reverse('student:upload', kwargs={'class_id': self._class.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_raises_403_on_admin_without_access(self):
        admin_without_access = AdministrationMember(
            first_name='test',
            last_name='test',
            username='user1',
            email='user1@mail.com',
        )
        admin_without_access.set_password('testpass123')
        admin_without_access.save()
        self.client.login(username='user1', password='testpass123')
        url = reverse('student:upload', kwargs={'class_id': self._class.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_raises_403_on_teacher_without_access(self):
        teacher = Teacher(
            first_name='test',
            last_name='test',
            username='teacher',
            email='teacher@mail.com',
        )
        teacher.set_password('testpass123')
        teacher.save()
        self.client.login(username='teacher', password='testpass123')
        url = reverse('student:upload', kwargs={'class_id': self._class.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_view_ok_response(self):
        self.client.login(username='user', password='testpass123')
        url = reverse('student:upload', kwargs={'class_id': self._class.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/upload.html')
        self.assertEqual(response.context.get('class'), self._class)

    def test_form(self):
        self.client.login(username='user', password='testpass123')
        url = reverse('student:upload', kwargs={'class_id': self._class.id})
        response = self.client.get(url)
        self.assertIsInstance(response.context.get('form'), StudentExcelUploadForm)

    def test_upload_invalid_excel(self):
        self.client.login(username='user', password='testpass123')
        url = reverse('student:upload', kwargs={'class_id': self._class.id})
        df = pd.DataFrame({'first_name': ['John'], 'last_name': ['Snow']})
        content = BytesIO()
        writer = pd.ExcelWriter(content, engine='xlsxwriter')
        df.to_excel(writer)
        writer.save()
        content.seek(0)
        invalid_excel = SimpleUploadedFile('invalid.xlsx', content.read())
        response = self.client.post(url, data={'file': invalid_excel})
        self.assertContains(response, 'Invalid data in excel file')

    def test_upload_not_excel(self):
        self.client.login(username='user', password='testpass123')
        url = reverse('student:upload', kwargs={'class_id': self._class.id})
        pdf_file = SimpleUploadedFile('file.pdf', b'Some text')
        response = self.client.post(url, data={'file': pdf_file})
        self.assertContains(response, 'File extension “pdf” is not allowed. Allowed extensions are: xlsx.')

    def test_upload_correct_excel(self):
        self.client.login(username='user', password='testpass123')
        url = reverse('student:upload', kwargs={'class_id': self._class.id})
        df = pd.DataFrame({'order_in_class': [1], 'first_name': ['John'], 'last_name': ['Snow'], 'email': [None],
                           'phone_number': [None]})
        content = BytesIO()
        writer = pd.ExcelWriter(content, engine='xlsxwriter')
        df.to_excel(writer)
        writer.save()
        content.seek(0)
        excel = SimpleUploadedFile('invalid.xlsx', content.read())
        response = self.client.post(url, data={'file': excel})
        self.assertRedirects(response, self._class.get_absolute_url())
        self.assertEqual(self._class.students.count(), 1)
