""" Unit tests for forms.py """
from django.test import TestCase
from django.contrib.auth.models import User
from iPoorly.models import Category, Heading, AgeGroup, Child
from iPoorly.forms import LoginForm, SignUpForm, AddChildForm, EditChildForm, CategoryEditForm, HeadingEditForm,\
SubHeadingEditForm, SearchForm, DiaryLogEditForm, ForgotPassword

class LoginFormTest(TestCase):
    """ unit test for the fields in the login form """

    def test_username_field_label(self):
        """ test label shown by form for username is correct """
        form = LoginForm()
        self.assertTrue(form.fields['username'].label == 'Username')

    def test_password_field_label(self):
        """ test label shown by form for password is correct """
        form = LoginForm()
        self.assertTrue(form.fields['password'].label == 'Password')

    def test_username_over_100_char(self):
        """ test that form is not accepted with username greater than 100 chars """
        username = 'a'*101
        password = 'password'
        form_data = {'username': username, 'password':password}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['Ensure this value has at most 100 characters (it has 101).'],
        })

    def test_password_is_required(self):
        """ test that form is not valid if password is not given """
        username = 'username'
        form_data = {'username': username}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_is_required(self):
        """ test that form is not valid if user is not given """
        password = 'password'
        form_data = {'password': password}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_is_accepted(self):
        """ test that form is accepted with correct data format """
        username = 'username'
        password = 'password'
        form_data = {'username': username, 'password':password}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = LoginForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
        })

class SignUpFormTest(TestCase):
    """ unit test for the fields in the sign up form """

    def test_username_field_label(self):
        """ test label shown by form for username is correct """
        form = SignUpForm()
        self.assertTrue(form.fields['username'].label == 'Username')

    def test_password_field_label(self):
        """ test label shown by form for password is correct """
        form = SignUpForm()
        self.assertTrue(form.fields['password'].label == 'Password')

    def test_email_field_label(self):
        """ test label shown by form for email is correct """
        form = SignUpForm()
        self.assertTrue(form.fields['email'].label == 'Email')

    def test_username_over_100_char(self):
        """ test that form is not accepted with username greater than 100 chars """
        username = 'a'*101
        password = 'password'
        email = 'email@email.com'
        form_data = {'username': username, 'password':password, 'email':email}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['Ensure this value has at most 100 characters (it has 101).'],
        })

    def test_password_is_required(self):
        """ test that form is not valid if password is not given """
        username = 'username'
        email = 'email@email.com'
        form_data = {'username': username, 'email':email}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_is_required(self):
        """ test that form is not valid if user is not given """
        password = 'password'
        email = 'email@email.com'
        form_data = {'password': password, 'email':email}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_is_required(self):
        """ test that form is not valid if email is not given """
        password = 'password'
        username = 'username'
        form_data = {'username': username, 'password': password}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_is_accepted(self):
        """ test that form is accepted with correct data format """
        username = 'username'
        password = 'password'
        email = 'email@email.com'
        form_data = {'username': username, 'password':password, 'email':email}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = SignUpForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
            'email': ['This field is required.'],
        })

class ForgotPasswordTest(TestCase):
    """ unit test for the fields in the forgot password form """
    def test_username_field_label(self):
        """ test label shown by form for username is correct """
        form = ForgotPassword()
        self.assertTrue(form.fields['username'].label == 'Username')

    def test_password_field_label(self):
        """ test label shown by form for password is correct """
        form = ForgotPassword()
        self.assertTrue(form.fields['password'].label == 'New Password')

    def test_email_field_label(self):
        """ test label shown by form for email is correct """
        form = ForgotPassword()
        self.assertTrue(form.fields['email'].label == 'Email')
    def test_username_over_100_char(self):
        """ test that form is not accepted with username greater than 100 chars """
        username = 'a'*101
        password = 'password'
        email = 'email@email.com'
        form_data = {'username': username, 'password':password, 'email':email}
        form = ForgotPassword(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['Ensure this value has at most 100 characters (it has 101).'],
        })

    def test_password_is_required(self):
        """ test that form is not valid if password is not given """
        username = 'username'
        email = 'email@email.com'
        form_data = {'username': username, 'email':email}
        form = ForgotPassword(data=form_data)
        self.assertFalse(form.is_valid())

    def test_username_is_required(self):
        """ test that form is not valid if user is not given """
        password = 'password'
        email = 'email@email.com'
        form_data = {'password': password, 'email':email}
        form = ForgotPassword(data=form_data)
        self.assertFalse(form.is_valid())

    def test_email_is_required(self):
        """ test that form is not valid if email is not given """
        password = 'password'
        username = 'username'
        form_data = {'username': username, 'password': password}
        form = ForgotPassword(data=form_data)
        self.assertFalse(form.is_valid())

    def test_is_accepted(self):
        """ test that form is accepted with correct data format """
        username = 'username'
        password = 'password'
        email = 'email@email.com'
        form_data = {'username': username, 'password':password, 'email':email}
        form = ForgotPassword(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = SignUpForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
            'email': ['This field is required.'],
        })

class AddChildFormTest(TestCase):
    """ unit test for the fields in the add child form """

    def test_name_field_label(self):
        """ test label shown by form for childname is correct """
        form = AddChildForm()
        self.assertTrue(form.fields['childName'].label == 'Child Name')

    def test_dob_field_label(self):
        """ test label shown by form for dob is correct """
        form = AddChildForm()
        self.assertTrue(form.fields['dob'].label == 'Child Date of Birth')

    def test_child_name_over_100_char(self):
        """ test that form is not accepted with child name greater than 100 chars """
        child_name = 'a'*101
        dob = '2016-05-05'
        form_data = {'childName': child_name, 'dob':dob}
        form = AddChildForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'childName': ['Ensure this value has at most 100 characters (it has 101).'],
        })
    def test_child_age_over_5_years(self):
        """ test that form is not accepted with child age greater than 5 years """
        child_name = 'a'
        dob = '2000-05-05'
        form_data = {'childName': child_name, 'dob':dob}
        form = AddChildForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_child_name_is_required(self):
        """ test that form is not valid if child name is not given """
        dob = '2016-05-05'
        form_data = {'dob':dob}
        form = AddChildForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_dob_is_required(self):
        """ test that form is not valid if dob is not given """
        child_name = 'Bob'
        form_data = {'childName': child_name}
        form = AddChildForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_is_accepted(self):
        """ test that form is accepted with correct data format """
        child_name = 'Bob'
        dob = '2016-05-05'
        form_data = {'childName': child_name, 'dob':dob}
        form = AddChildForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = AddChildForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'childName': ['This field is required.'],
            'dob': ['This field is required.'],
        })

class EditChildFormFormTest(TestCase):
    """ unit test for the fields in the edit child form """

    def test_child_name_field_label(self):
        """ test label shown by form for childname is correct """
        form = EditChildForm()
        self.assertTrue(form.fields['childName'].label == 'Child Name')

    def test_dob_field_label(self):
        """ test label shown by form for dob is correct """
        form = EditChildForm()
        self.assertTrue(form.fields['dob'].label == 'Child Date of Birth')

    def test_child_name_over_100_char(self):
        """ test that form is not accepted with child name greater than 100 chars """
        child_name = 'a'*101
        dob = '2016-05-05'
        child_id = 0
        form_data = {'childName': child_name, 'dob':dob, 'childID':child_id}
        form = EditChildForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'childName': ['Ensure this value has at most 100 characters (it has 101).'],
        })

    def test_child_age_over_5_years(self):
        """ test that form is not accepted with child age greater than 5 years """
        child_name = 'a'
        dob = '2000-05-05'
        form_data = {'childName': child_name, 'dob':dob}
        form = AddChildForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_child_name_is_required(self):
        """ test that form is not valid if child name is not given """
        dob = '2016-05-05'
        child_id = 0
        form_data = {'dob':dob, 'childID':child_id}
        form = EditChildForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_dob_is_required(self):
        """ test that form is not valid if dob is not given """
        child_name = 'Bob'
        child_id = 0
        form_data = {'childName': child_name, 'childID':child_id}
        form = EditChildForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_is_accepted(self):
        """ test that form is accepted with correct data format """
        child_name = 'Bob'
        dob = '2016-05-05'
        form_data = {'childName': child_name, 'dob':dob}
        form = AddChildForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = AddChildForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'childName': ['This field is required.'],
            'dob': ['This field is required.'],
        })

class CategoryEditFormTest(TestCase):
    """ unit test for the fields in the category edit form """

    def test_category_name_field_label(self):
        """ test label shown by form for category name is correct """
        form = CategoryEditForm()
        self.assertTrue(form.fields['categoryName'].label == 'Symptom Name')

    def test_description_field_label(self):
        """ test label shown by form for description is correct """
        form = CategoryEditForm()
        self.assertTrue(form.fields['description'].label == 'Description/Summary')

    def test_is_accepted(self):
        """ test that form is accepted with correct data format and object is saved in the database """
        form = CategoryEditForm({
            'categoryName': 'Test Name',
            'description': 'Test description',
        })
        self.assertTrue(form.is_valid())
        category = form.save()
        self.assertEqual(category.categoryName, 'test_name')
        self.assertEqual(category.description, 'Test description')

    def test_accepted_without_descript(self):
        """ test that form is accepted with correct data format (without description) and object is saved in the database """
        form = CategoryEditForm({
            'categoryName': 'Test Name',
        })
        self.assertTrue(form.is_valid())
        category = form.save()
        self.assertEqual(category.categoryName, 'test_name')

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = CategoryEditForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'categoryName': ['This field is required.'],
        })

class HeadingEditFormTest(TestCase):
    """ unit test for the fields in the heading edit form """

    def setUp(self):
        self.category = Category.objects.create(categoryName='Test Heading Form', description='This is a test for Heading Form')

    def test_category_name_field_label(self):
        """ test label shown by form for category name is correct """
        form = HeadingEditForm()
        self.assertTrue(form.fields['categoryName'].label == 'Symptom')

    def test_text_field_label(self):
        """ test label shown by form for text is correct """
        form = HeadingEditForm()
        self.assertTrue(form.fields['text'].label == 'Heading Title')

    def test_is_accepted(self):
        """ test that form is accepted with correct data format and object is saved in the database """
        form = HeadingEditForm({
            'categoryName': self.category.pk,
            'text': 'Test Heading in Form',
        })
        self.assertTrue(form.is_valid())
        heading = form.save()
        self.assertEqual(heading.categoryName, self.category)
        self.assertEqual(heading.text, 'Test Heading in Form')

    def test_text_over_500_char(self):
        """ test that form is not accepted with text greater than 500 chars """
        form = HeadingEditForm({
            'categoryName': self.category.pk,
            'text': 'a'*501,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'text': ['Ensure this value has at most 500 characters (it has 501).'],
        })

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = HeadingEditForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'categoryName': ['This field is required.'],
            'text': ['This field is required.'],
        })

class SubHeadingEditFormTest(TestCase):
    """ unit test for the fields in the sub heading edit form """

    def setUp(self):
        category = Category.objects.create(categoryName='Test Sub Heading Form', description='This is a test for Heading Form')
        self.heading = Heading.objects.create(categoryName=category, text='This is a test for Sub Heading Edit Form')
        self.age_group = AgeGroup.objects.create(age_group=0)

    def test_field_label(self):
        """ test label shown by form for heading id is correct """
        form = SubHeadingEditForm()
        self.assertTrue(form.fields['headingId'].label == 'Heading')

    def test_sub_title_field_label(self):
        """ test label shown by form for title is correct """
        form = SubHeadingEditForm()
        self.assertTrue(form.fields['title'].label == 'Title')

    def test_sub_text_field_label(self):
        """ test label shown by form for text is correct """
        form = SubHeadingEditForm()
        self.assertTrue(form.fields['text'].label == 'Content')

    def test_is_accepted(self):
        """ test that form is accepted with correct data format and object is saved in the database """
        form = SubHeadingEditForm({
            'headingId': self.heading.pk,
            'title': 'Sub Heading Form Title',
            'text': 'Test Sub Heading in Form',
            'ageGroup': [self.age_group.pk],
        })
        self.assertTrue(form.is_valid())
        sub_heading = form.save()
        self.assertEqual(sub_heading.headingId, self.heading)
        self.assertEqual(sub_heading.title, 'Sub Heading Form Title')
        self.assertEqual(sub_heading.text, 'Test Sub Heading in Form')
        self.assertEqual(sub_heading.ageGroup.get(pk=self.age_group.pk), self.age_group)

    def test_title_over_150_char(self):
        """ test that form is not accepted with title greater than 150 chars """
        form = SubHeadingEditForm({
            'headingId': self.heading.pk,
            'title': 'a'*151,
            'text': 'Test Sub Heading in Form',
            'ageGroup': [self.age_group.pk],
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'title': ['Ensure this value has at most 150 characters (it has 151).'],
        })

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = SubHeadingEditForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'headingId': ['This field is required.'],
            'title': ['This field is required.'],
            'text': ['This field is required.'],
            'ageGroup':['This field is required.'],
        })

class SearchFormTest(TestCase):
    """ unit test for the fields in the search form """

    def test_query_field_label(self):
        """ test label shown by form for query is correct """
        form = SearchForm()
        self.assertTrue(form.fields['query'].label == 'Search Query')

    def test_username_over_100_char(self):
        """ test that form is not accepted with title greater than 100 chars """
        query = 'a'*151
        form_data = {'query': query}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'query': ['Ensure this value has at most 150 characters (it has 151).'],
        })

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = SearchForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'query': ['This field is required.'],
        })

    def test_is_accepted(self):
        """ test that form is accepted with correct data format """
        query = 'search query'
        form_data = {'query': query}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

class DiaryLogEditFormTest(TestCase):
    """ unit test for the fields in the diary log edit form """

    def setUp(self):
        user = User.objects.create(username='Test', password='Test')
        self.child = Child.objects.create(username=user, childName='Test Child in Form', dob='2017-06-26', activate=True)

    def test_is_accepted(self):
        """ test that form is accepted with correct data format and object is saved in the database """
        form = DiaryLogEditForm({
            'child': self.child.pk,
            'title': 'Test Title',
            'text': 'Test dilary log made using form',
            'check_id': 5,
        })
        self.assertTrue(form.is_valid())
        diary_log = form.save()
        self.assertEqual(diary_log.child, self.child)
        self.assertEqual(diary_log.text, 'Test dilary log made using form')
        self.assertEqual(diary_log.title, 'Test Title')

    def test_blank_data(self):
        """ test form is not valid with blank data """
        form = DiaryLogEditForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'child': ['This field is required.'],
            'text': ['This field is required.'],
            'title': ['This field is required.'],
            'check_id': ['This field is required.'],
        })
