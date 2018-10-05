""" Unit tests for models.py """
from django.test import TestCase
from django.contrib.auth.models import User
from iPoorly.models import Child, Category, Heading, AgeGroup, SubHeading, DiaryLog


class ChildModelTest(TestCase):
    """ unit tests for the child model """

    def setUp(self):
        user = User.objects.create(username='Test', password='Test')
        child = Child.objects.create(username=user, childName='Test Child', dob='2017-06-26')
        self.child_pk = child.pk

    def test_child_name_label(self):
        """ test if the child name field has the correct label """
        child = Child.objects.get(id=self.child_pk)
        field_label = child._meta.get_field('childName').verbose_name
        self.assertEqual(field_label, 'childName')

    def test_dob_label(self):
        """ test if the date of birth field has the correct label """
        child = Child.objects.get(id=self.child_pk)
        field_label = child._meta.get_field('dob').verbose_name
        self.assertEqual(field_label, 'dob')

    def test_activate_label(self):
        """ test if the activate field has the correct label """
        child = Child.objects.get(id=self.child_pk)
        field_label = child._meta.get_field('activate').verbose_name
        self.assertEqual(field_label, 'activate')

    def test_object_name_is_child_name(self):
        """ test if the __str__ function returns the right string """
        child = Child.objects.get(id=self.child_pk)
        expected_object_name = '%s' % (child.childName)
        self.assertEqual(expected_object_name, str(child))

class CategoryModelTest(TestCase):
    """ unit tests for the category model """

    def setUp(self):
        category = Category.objects.create(categoryName='Test', description='This is a test for Category Model')
        self.category_pk = category.pk

    def test_category_name_label(self):
        """ test if the category name field has the correct label """
        category = Category.objects.get(categoryId=self.category_pk)
        field_label = category._meta.get_field('categoryName').verbose_name
        self.assertEqual(field_label, 'Symptom Name')

    def test_description_label(self):
        """ test if the description field has the correct label """
        category = Category.objects.get(categoryId=self.category_pk)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Description/Summary')

    def test_category_name_max_length(self):
        """ test if the max length of category name is correct """
        category = Category.objects.get(categoryId=self.category_pk)
        max_length = category._meta.get_field('categoryName').max_length
        self.assertEqual(max_length, 150)

    def test_object_name_category_name(self):
        """ test if the __str__ function returns the right string """
        category = Category.objects.get(categoryId=self.category_pk)
        expected_object_name = '%s' % (category.categoryName.replace('_', ' ').title())
        self.assertEqual(expected_object_name, str(category))

    def test_object_url(self):
        """ test if the object url (get_absolute_url function) returns the right url """
        category = Category.objects.get(categoryId=self.category_pk)
        expected_object_url = '/symptom/%s' % (category.categoryName)
        self.assertEqual(expected_object_url, category.get_absolute_url())

class HeadingModelTest(TestCase):
    """ unit tests for the heading model """

    def setUp(self):
        category = Category.objects.create(categoryName='Test', description='This is a test for Category Model')
        heading = Heading.objects.create(categoryName=category, text='This is a test for Heading Model')
        self.heading_pk = heading.pk

    def test_category_name_label(self):
        """ test if the category name field has the correct label """
        heading = Heading.objects.get(headingId=self.heading_pk)
        field_label = heading._meta.get_field('categoryName').verbose_name
        self.assertEqual(field_label, 'Symptom')

    def test_text_label(self):
        """ test if the text field has the correct label """
        heading = Heading.objects.get(headingId=self.heading_pk)
        field_label = heading._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'Heading Title')

    def test_heading_text_max_length(self):
        """ test if the max length of text is correct """
        heading = Heading.objects.get(headingId=self.heading_pk)
        max_length = heading._meta.get_field('text').max_length
        self.assertEqual(max_length, 500)

    def test_object_name_heading_text(self):
        """ test if the __str__ function returns the right string """
        heading = Heading.objects.get(headingId=self.heading_pk)
        expected_object_name = '%s' % (heading.text)
        self.assertEqual(expected_object_name, str(heading))

    def test_object_url(self):
        """ test if the object url (get_absolute_url function) returns the right url """
        heading = Heading.objects.get(headingId=self.heading_pk)
        expected_object_url = '/symptom/information/%d' % (heading.headingId)
        self.assertEqual(expected_object_url, heading.get_absolute_url())

class AgeGroupModelTest(TestCase):
    """ unit tests for the age group model """

    def setUp(self):
        age_group = AgeGroup.objects.create(age_group=0)
        self.age_group_pk = age_group.pk

    def test_age_group_label(self):
        """ test if the age group field has the correct label """
        age_group = AgeGroup.objects.get(id=self.age_group_pk)
        field_label = age_group._meta.get_field('age_group').verbose_name
        self.assertEqual(field_label, 'Age Group')

    def test_object_name_is_age_group(self):
        """ test if the __str__ function returns the right string """
        age_group = AgeGroup.objects.get(id=self.age_group_pk)
        expected_object_name = '%s' % (age_group.get_age_group_display())
        self.assertEqual(expected_object_name, str(age_group))

class SubHeadingModelTest(TestCase):
    """ unit tests for the sub heading model """

    def setUp(self):
        agegroup = AgeGroup.objects.create(age_group=0)
        category = Category.objects.create(categoryName='Test', description='This is a test for Category Model')
        heading = Heading.objects.create(categoryName=category, text='This is a test for Heading Model')
        sub_heading = SubHeading.objects.create(headingId=heading, title='Sub heading test title', text='Sub heading test text')
        sub_heading.ageGroup.add(agegroup)
        self.sub_heading_pk = sub_heading.pk

    def test_heading_id_label(self):
        """ test if the heading id field has the correct label """
        subheading = SubHeading.objects.get(subHeadingId=self.sub_heading_pk)
        field_label = subheading._meta.get_field('headingId').verbose_name
        self.assertEqual(field_label, 'Heading')

    def test_title_label(self):
        """ test if the title field has the correct label """
        subheading = SubHeading.objects.get(subHeadingId=self.sub_heading_pk)
        field_label = subheading._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Title')

    def test_text_label(self):
        """ test if the test field has the correct label """
        subheading = SubHeading.objects.get(subHeadingId=self.sub_heading_pk)
        field_label = subheading._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'Content')

    def test_title_max_length(self):
        """ test if the max length of title is correct """
        subheading = SubHeading.objects.get(subHeadingId=self.sub_heading_pk)
        max_length = subheading._meta.get_field('title').max_length
        self.assertEqual(max_length, 150)

    def test_object_url(self):
        """ test if the object url (get_absolute_url function) returns the right url """
        subheading = SubHeading.objects.get(subHeadingId=self.sub_heading_pk)
        expected_object_url = '/symptom/information/%d#%d' % (subheading.headingId.headingId, subheading.subHeadingId)
        self.assertEqual(expected_object_url, subheading.get_absolute_url())

    def test_object_name_category_name(self):
        """ test if the __str__ function returns the right string """
        subheading = SubHeading.objects.get(subHeadingId=self.sub_heading_pk)
        expected_object_name = '%s (%s)' % (subheading.title, ", ".join([str(x) for x in subheading.ageGroup.all()]))
        self.assertEqual(expected_object_name, str(subheading))

class DiaryLogModelTest(TestCase):
    """ unit tests for the diary log model """

    def setUp(self):
        user = User.objects.create(username='Test', password='Test')
        child = Child.objects.create(username=user, childName='Test Child', dob='2017-06-26')
        diary_log = DiaryLog.objects.create(child=child, text='Test diary log entry/text')
        self.diary_log_pk = diary_log.pk

    def test_text_label(self):
        """ test if the text field has the correct label """
        diary_log = DiaryLog.objects.get(diary_id=self.diary_log_pk)
        field_label = diary_log._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'Diary Entry')

    def test_title_label(self):
        """ test if the text field has the correct label """
        diary_log = DiaryLog.objects.get(diary_id=self.diary_log_pk)
        field_label = diary_log._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Title')
