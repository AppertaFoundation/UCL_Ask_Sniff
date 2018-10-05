""" Unit tests for models.py """
import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from iPoorly.models import Child, DiaryLog, Category, Heading, SubHeading, AgeGroup
from iPoorly.forms import HeadingEditForm, SubHeadingEditForm

class IndexView(TestCase):
    """ unit tests for the index view """

    def setUp(self):
        self.user = User.objects.create_user(username='IndexTest', password='Test')
        self.child = Child.objects.create(username=self.user, childName='ChildView Child', dob='2017-06-26', activate=True)
        AgeGroup.objects.create(age_group=0)

    def test_view_page(self):
        """ test the page for the view """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """ test the correct template is used for the view """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_view_logged_in_already(self):
        """ test that a logged in user is redirected to disclaimer """
        self.client.login(username='IndexTest', password='Test')
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('disclaimer'))
        self.assertTemplateUsed(response, 'disclaimer.html')

    def test_view_age_selected_already(self):
        """ test that a one time user with an age already selected is redirected to disclaimer """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('disclaimer'))
        self.assertTemplateUsed(response, 'disclaimer.html')

    def test_logged_in_disclaimer_read(self):
        """ test that a logged in user who has read the disclaimer is redirected to homepage """
        session = self.client.session
        session['disclaimer'] = True
        session.save()
        self.client.login(username='IndexTest', password='Test')
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTemplateUsed(response, 'homepage.html')

    def test_age_range_disclaimer_read(self):
        """ test that a one time user with an age already selected and disclaimer read is redirected to homepage """
        session = self.client.session
        session['disclaimer'] = True
        session['age_range'] = 0
        session.save()
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTemplateUsed(response, 'homepage.html')

class HomepageView(TestCase):
    """ unit tests for the index view """

    def setUp(self):
        self.user = User.objects.create_user(username='HomepageTest', password='Test')
        self.child = Child.objects.create(username=self.user, childName='HomepageTest Child', dob='2017-06-26', activate=True)
        AgeGroup.objects.create(age_group=0)

    def test_disclaimer_not_read(self):
        """ test that if discalimer is not read, redirection to disclaimer """
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('disclaimer'))
        self.assertTemplateUsed(response, 'disclaimer.html')

    def test_read_disclaimer_logged_in(self):
        """ test that if discalimer is read and user is logged in homepage is shown """
        session = self.client.session
        session['disclaimer'] = True
        session.save()
        self.client.login(username='HomepageTest', password='Test')
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'HomepageTest')
        self.assertTemplateUsed(response, 'homepage.html')

    def test_read_disclaimer_age_range(self):
        """ test that if discalimer is read and age range selected homepage is shown """
        session = self.client.session
        session['disclaimer'] = True
        session['age_range'] = 0
        session.save()
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_read_disclaim_no_age_user(self):
        """ test that if discalimer is read but user is not logged in or age range is not selected redirects to select age """
        session = self.client.session
        session['disclaimer'] = True
        session.save()
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('age'))
        self.assertTemplateUsed(response, 'age_select.html')

class UserLoginView(TestCase):
    """ unit tests for the user login view """

    def setUp(self):
        User.objects.create_user(username='UserLoginTest', password='Test', email='email@email.com')

    def test_correct_login_details(self):
        """ test that user is redirected to disclaimer is correct login credentials """
        response = self.client.post(reverse('user_login'), {'username':'UserLoginTest', 'password':'Test'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('disclaimer'))
        self.assertTemplateUsed(response, 'disclaimer.html')

    def test_incorrect_username(self):
        """ test user is sent back to index page if incorrect username """
        response = self.client.post(reverse('user_login'), {'username':'UserLogin', 'password':'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_incorrect_password(self):
        """ test user is sent back to index page if incorrect password """
        response = self.client.post(reverse('user_login'), {'username':'UserLoginTest', 'password':'Test123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_instead_of_post(self):
        """ test that user is redirected to index if they make a get call to this view """
        response = self.client.get(reverse('user_login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

class UserSignUpView(TestCase):
    """ unit tests for the user signup view """

    def setUp(self):
        Group.objects.get_or_create(name='Users')
        User.objects.create_user(username='SignUpTest', password='Test', email='email@email.com')

    def test_new_sign_up_details(self):
        """ test that user object is created if correct signup information is used """
        response = self.client.post(reverse('user_signup'), {'username':'SignUpTest2', 'password':'Test', 'email':'email@email.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('disclaimer'))
        self.assertTemplateUsed(response, 'disclaimer.html')
        user = User.objects.get(username='SignUpTest2')
        self.assertEqual(user.username, 'SignUpTest2')

    def test_existing_username(self):
        """ test that user is redirected to index if username selected for creating account already exists """
        response = self.client.post(reverse('user_signup'), {'username':'SignUpTest', 'password':'Test', 'email':'email@email.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_instead_of_post(self):
        """ test that user is redirected to index if they make a get call to this view """
        response = self.client.get(reverse('user_signup'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

class ForgotPasswordView(TestCase):
    """ unit tests for the forgot password view """

    def setUp(self):
        Group.objects.get_or_create(name='Users')
        User.objects.create_user(username='ForgotTest', password='Test', email='email@email.com')

    def test_correct_credentials(self):
        """ test that user's password is changed """
        response = self.client.post(reverse('forgot_password'), {'username':'ForgotTest', 'password':'Test2', 'email':'email@email.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))
        self.assertTemplateUsed(response, 'index.html')
        response = self.client.post(reverse('user_login'), {'username':'ForgotTest', 'password':'Test2'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('disclaimer'))
        self.assertTemplateUsed(response, 'disclaimer.html')
        self.client.get(reverse('user_logout'), follow=True)       

    def test_incorrect_username(self):
        """ test that user is redirected to forgot_password if username is wrong """
        response = self.client.post(reverse('forgot_password'), {'username':'Forgot', 'password':'Test', 'email':'email@email.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forgot_password.html')
        self.assertEqual(response.context['error'], 'Incorrect Username-Email combination')

    def test_incorrect_email(self):
        """ test that user is redirected to forgot_password if email is wrong """
        response = self.client.post(reverse('forgot_password'), {'username':'ForgotTest', 'password':'Test', 'email':'ema@email.com'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forgot_password.html')
        self.assertEqual(response.context['error'], 'Incorrect Username-Email combination')

class UserLogOutView(TestCase):
    """ unit tests for the user logout view """

    def setUp(self):
        User.objects.create_user(username='LogOutTest', password='Test', email='email@email.com')

    def test_log_out_when_logged_in(self):
        """ test user is logged out and redirected to index """
        self.client.login(username='LogOutTest', password='Test')
        response = self.client.get(reverse('user_logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

class AgeSelectView(TestCase):
    """ unit tests for the age view """

    def setUp(self):
        AgeGroup.objects.create(age_group=0)
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_view_page(self):
        """ test the page for the view """
        response = self.client.get(reverse('age'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'age_select.html')

    def test_select_an_age(self):
        """ test that the same age group selected is saved in session """
        response = self.client.post(reverse('age'), {'age':0}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTemplateUsed(response, 'homepage.html')
        session = self.client.session
        self.assertEqual(session['age_range'], '0')

class DisclaimerView(TestCase):
    """ unit tests for the disclaimer view """

    def setUp(self):
        self.user = User.objects.create_user(username='DisclaimerTest', password='Test', email='email@email.com')
        self.child = Child.objects.create(username=self.user, childName='DisclaimerTest Child', dob='2017-06-26', activate=True)
        AgeGroup.objects.create(age_group=0)
        session = self.client.session
        session['age_range'] = 0
        session.save()

    def test_view_page(self):
        """ test the page for the view """
        response = self.client.get(reverse('disclaimer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'disclaimer.html')

    def test_read_disclaim_logged_in(self):
        """ test if user that has logged in and read the disclaimer is redirected to homepage """
        self.client.login(username='DisclaimerTest', password='Test')
        response = self.client.post(reverse('disclaimer'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTemplateUsed(response, 'homepage.html')

    def test_read_disclaimer_one_time(self):
        """ test if one time user that has read the disclaimer is redirected to select age """
        response = self.client.post(reverse('disclaimer'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('age'))
        self.assertTemplateUsed(response, 'age_select.html')

class LocationMapView(TestCase):
    """ unit tests for the map view """

    def setUp(self):
        User.objects.create_user(username='LocationMapViewTest', password='Test', email='email@email.com')
        self.client.login(username='LocationMapViewTest', password='Test')
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_view_page(self):
        """ test the page for the view """
        response = self.client.get(reverse('map'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """ test that the correct template is used for the view """
        response = self.client.get(reverse('map'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map.html')

class ChildView(TestCase):
    """ unit tests for my_child, child_activate and child_delete view """

    def setUp(self):
        self.user = User.objects.create_user(username='ChildViewTest', password='Test', email='email@email.com')
        self.child = Child.objects.create(username=self.user, childName='ChildView Child', dob='2017-06-26', activate=True)
        session = self.client.session
        session['disclaimer'] = True
        session.save()
        self.client.login(username='ChildViewTest', password='Test')

    def test_view_page(self):
        """ test the page for the my_child view """
        response = self.client.get(reverse('myChild'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_child.html')
        self.assertIn(self.child, [x[0] for x in response.context['children']])

    def test_add_child(self):
        """ test that a new child is added for a user and shows up in the users my_child view page """
        response = self.client.post(reverse('myChild'), {'childName':'ChildView Child 2', 'dob':'2017-06-27', 'add':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_child.html')
        self.assertIn(self.child, [x[0] for x in response.context['children']])
        new_child = Child.objects.get(childName='ChildView Child 2')
        self.assertIn(new_child, [x[0] for x in response.context['children']])

    def test_edit_child(self):
        """ test that a child is edited for a user and edited object shows up in the users my_child view page """
        response = self.client.post(reverse('child_manage'), {'childName':'ChildView Child', 'dob':'2017-06-25', 'edit':'', 'childID':self.child.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'child_manage.html')
        edit_child = Child.objects.get(id=self.child.id)
        self.assertIn(edit_child, [x[0] for x in response.context['children']])
        self.assertNotEqual(self.child.dob, edit_child.dob)
        self.assertEqual(edit_child.dob, datetime.date(2017, 6, 25))

    def test_child_activate(self):
        """ test making a child as an active child for an user """
        self.child.activate = False
        self.child.save()
        self.assertFalse(self.child.activate)
        response = self.client.post(reverse('child_activate'), {'id':self.child.id})
        edit_child = Child.objects.get(id=self.child.id)
        self.assertTrue(edit_child.activate)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 1}
        )

    def test_child_delete(self):
        """ test that we can delete a child for a user """
        new_child = Child.objects.create(username=self.user, childName='ChildView Child Delete', dob='2017-06-26')
        response = self.client.post(reverse('child_delete'), {'id':new_child.id})
        self.assertRaises(Child.DoesNotExist, Child.objects.get, id=new_child.id)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 1}
        )
        response = self.client.get(reverse('myChild'))
        self.assertNotIn(new_child, response.context['children'])

class DiaryView(TestCase):
    """ unit tests for diary, diary_logs and diary_delete view """

    def setUp(self):
        self.user = User.objects.create_user(username='DiaryViewTest', password='Test', email='email@email.com')
        self.child = Child.objects.create(username=self.user, childName='DiaryView Child', dob='2017-06-26', activate=True)
        session = self.client.session
        session['disclaimer'] = True
        session.save()
        self.client.login(username='DiaryViewTest', password='Test')
        self.diary_log_1 = DiaryLog.objects.create(child=self.child, text='Diary Entry 1')

    def test_view_page(self):
        """ test the page for the diary view """
        response = self.client.get(reverse('diary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diary.html')
        self.assertIn(self.child, response.context['children'])

    def test_view_diary_logs_of_child(self):
        """ test that all diary logs of a child is shown using the correct template """
        response = self.client.get(reverse('diary_logs', kwargs={'child_id':self.child.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diary_logs.html')
        self.assertIn(self.diary_log_1, response.context['logs'])

    def test_add_new_diary_log(self):
        """ test adding a diary log for a child """
        response = self.client.post(reverse('diary_logs', kwargs={'child_id':self.child.id}), \
        {'check_id':'0', 'child':self.child.pk, 'text':'Diary Entry 2', 'title':'Test title'})
        self.assertEqual(response.status_code, 200)
        diary_log_2 = DiaryLog.objects.get(text='Diary Entry 2')
        self.assertTemplateUsed(response, 'diary_logs.html')
        self.assertIn(self.diary_log_1, response.context['logs'])
        self.assertIn(diary_log_2, response.context['logs'])

    def test_edit_diary_log(self):
        """ test editing diary log of a child """
        response = self.client.post(reverse('diary_logs', kwargs={'child_id':self.child.id}), \
        {'check_id':self.diary_log_1.pk, 'child':self.child.pk, 'text':'Edited Diary Entry 1', 'title':'Test title'})
        self.assertEqual(response.status_code, 200)
        edited_diary_log_1 = DiaryLog.objects.get(diary_id=self.diary_log_1.diary_id)
        self.assertTemplateUsed(response, 'diary_logs.html')
        self.assertIn(edited_diary_log_1, response.context['logs'])
        self.assertEqual(edited_diary_log_1.text, 'Edited Diary Entry 1')
        self.assertNotEqual(edited_diary_log_1.text, self.diary_log_1.text)

    def test_delete_diary_log(self):
        """ test that we can delete a log for a child """
        new_diary_log = DiaryLog.objects.create(child=self.child, text='Diary Entry 3 to be deleted')
        response = self.client.post(reverse('diary_delete'), {'id':new_diary_log.diary_id})
        self.assertRaises(DiaryLog.DoesNotExist, DiaryLog.objects.get, diary_id=new_diary_log.diary_id)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 1}
        )
        response = self.client.get(reverse('diary_logs', kwargs={'child_id':self.child.id}))
        self.assertNotIn(new_diary_log, response.context['logs'])

class SearchView(TestCase):
    """ unit tests for the search view """

    def setUp(self):
        self.user = User.objects.create_user(username='SearchViewTest', password='Test', email='email@email.com')
        Child.objects.create(username=self.user, childName='ChildView Child', dob='2010-06-26', activate=True)
        agegroup = AgeGroup.objects.create(age_group=0)
        self.category = Category.objects.create(categoryName='SearchViewTest', description='This is a test for Search View')
        self.heading = Heading.objects.create(categoryName=self.category, text='This is a test for Search View')
        self.sub_heading = SubHeading.objects.create(headingId=self.heading, title='Search View test title', text='Search View test text')
        self.sub_heading.ageGroup.add(agegroup)
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_view_page_with_user(self):
        """ test the page for the view with a logged in user """
        self.client.login(username='SearchViewTest', password='Test')
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.client.logout()

    def test_view_page_age_range(self):
        """ test the page for the view with a one time user """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        self.client.login(username='SearchViewTest', password='Test')
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_search_category_user(self):
        """ test we can search for a category as a logged in user """
        self.client.login(username='SearchViewTest', password='Test')
        response = self.client.post(reverse('search'), {'search':self.category.categoryName})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_descrip_with_user(self):
        """ test we can search for a category description as a logged in user """
        self.client.login(username='SearchViewTest', password='Test')
        response = self.client.post(reverse('search'), {'search':self.category.description})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_heading_user(self):
        """ test we can search for a category description as a logged in user """
        self.client.login(username='SearchViewTest', password='Test')
        response = self.client.post(reverse('search'), {'search':self.heading.text})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_subhead_text_user(self):
        """ test we can search for sub heading text as a logged in user """
        self.client.login(username='SearchViewTest', password='Test')
        response = self.client.post(reverse('search'), {'search':self.sub_heading.text})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_subhead_title_user(self):
        """ test we can search for sub heading title as a logged in user """
        self.client.login(username='SearchViewTest', password='Test')
        response = self.client.post(reverse('search'), {'search':self.sub_heading.title})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_cat_age_range(self):
        """ test we can search for a category as a one time user """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        response = self.client.post(reverse('search'), {'search':self.category.categoryName})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_descript_age_range(self):
        """ test we can search for a category description as a one time user """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        response = self.client.post(reverse('search'), {'search':self.category.description})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_heading_age_range(self):
        """ test we can search for a heading as a one time user """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        response = self.client.post(reverse('search'), {'search':self.heading.text})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_subhead_text_age(self):
        """ test we can search for a sub heading text as a one time user """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        response = self.client.post(reverse('search'), {'search':self.sub_heading.text})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

    def test_search_subhead_title_age(self):
        """ test we can search for a sub heading title as a one time user """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        response = self.client.post(reverse('search'), {'search':self.sub_heading.title})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'data': [{'sub_heading_id':str(self.sub_heading.subHeadingId), 'text':self.sub_heading.text, 'title':self.sub_heading.title, \
            'heading_id':str(self.heading.headingId)}], 'status':1}
        )

class SymptomView(TestCase):
    """ unit tests for the symptom and symptom_heading view """

    def setUp(self):
        self.user = User.objects.create_user(username='SymptomViewTest', password='Test', email='email@email.com')
        self.child = Child.objects.create(username=self.user, childName='ChildView Child', dob='2010-06-26', activate=True)
        agegroup = AgeGroup.objects.create(age_group=0)
        self.category = Category.objects.create(categoryName='SymptomViewTest', description='This is a test for Symptom View')
        self.heading = Heading.objects.create(categoryName=self.category, text='This is a test for Symptom View')
        self.sub_heading = SubHeading.objects.create(headingId=self.heading, title='Symptom View test title', text='Symptom View test text')
        self.sub_heading.ageGroup.add(agegroup)
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_view_page_user(self):
        """ test the page for the symptom view with a logged in user """
        self.client.login(username='SymptomViewTest', password='Test')
        response = self.client.get(reverse('symptom', kwargs={'symptom_name': self.category}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'symptom.html')
        self.assertListEqual([self.heading], list(response.context['headings']))
        self.assertEqual(self.category.description, response.context['description'])

    def test_view_page_age_group(self):
        """ test the page for the symptom view with as a one time user """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        response = self.client.get(reverse('symptom', kwargs={'symptom_name': self.category}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'symptom.html')
        self.assertListEqual([self.heading], list(response.context['headings']))
        self.assertEqual(self.category.description, response.context['description'])

    def test_symptom_heading_user(self):
        """ test all headings for a symptom are shown in the template rendered by the view as a logged in user """
        self.client.login(username='SymptomViewTest', password='Test')
        response = self.client.get(reverse('symptom_heading', kwargs={'heading_id': self.heading.headingId}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'heading.html')
        self.assertEqual(self.heading, response.context['heading'])
        self.assertListEqual([self.sub_heading], list(response.context['subHeadings']))

    def test_symptom_heading_age_group(self):
        """ test all headings for a symptom are shown in the template rendered by the view as a one time user """
        session = self.client.session
        session['age_range'] = 0
        session.save()
        response = self.client.get(reverse('symptom_heading', kwargs={'heading_id': self.heading.headingId}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'heading.html')
        self.assertEqual(self.heading, response.context['heading'])
        self.assertListEqual([self.sub_heading], list(response.context['subHeadings']))

class AdminView(TestCase):
    """ unit test for the admin view """

    def setUp(self):
        Group.objects.create(name='Editors')
        editors_group = Group.objects.get(name='Editors')
        self.admin = User.objects.create_user(username='AdminViewTest', password='Test', email='email@email.com')
        self.admin.groups.add(editors_group)
        self.client.login(username='AdminViewTest', password='Test')
        self.category = Category.objects.create(categoryName='AdminViewTest', description='This is a test for Admin View')
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_view_page(self):
        """ test the page for the admin view """
        response = self.client.get(reverse('admin'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.category, response.context['categories'])
        self.assertTemplateUsed(response, 'admin.html')

    def test_add_category(self):
        """ test adding a category using admin panel """
        response = self.client.post(reverse('admin'), {'categoryName': 'New Category', 'description': 'This is a new category'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.category, response.context['categories'])
        new_category = Category.objects.get(categoryName='new_category')
        self.assertIn(new_category, response.context['categories'])

    def test_edit_category(self):
        """ test editing category """
        response = self.client.post(reverse('admin'), {'categoryName':self.category.categoryName, 'description':'New description',\
        'edit':'edit', 'id':self.category.categoryId}, follow=True)
        self.assertEqual(response.status_code, 200)
        edited_category_1 = Category.objects.get(categoryId=self.category.categoryId)
        self.assertEqual(edited_category_1.description, 'New description')
        self.assertNotEqual(edited_category_1.description, self.category.description)

    def test_delete_diary_log(self):
        """ test that we can delete a category """
        new_category = Category.objects.create(categoryName='AdminViewTest2', description='This is a test for Admin View')
        response = self.client.post(reverse('symptom_delete'), {'id':new_category.categoryId})
        self.assertRaises(Category.DoesNotExist, Category.objects.get, categoryId=new_category.categoryId)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 1, 'id':new_category.categoryId}
        )

class AdminSymptomView(TestCase):
    """ unit test for the admin_symptom view """

    def setUp(self):
        Group.objects.create(name='Editors')
        editors_group = Group.objects.get(name='Editors')
        self.admin = User.objects.create_user(username='AdminSymptomViewTest', password='Test', email='email@email.com')
        self.admin.groups.add(editors_group)
        self.client.login(username='AdminSymptomViewTest', password='Test')
        agegroup = AgeGroup.objects.create(age_group=0)
        self.category = Category.objects.create(categoryName='AdminSymptomViewTest', description='This is a test for AdminSymptom View')
        self.heading = Heading.objects.create(categoryName=self.category, text='This is a test for Admin symptom View')
        self.sub_heading = SubHeading.objects.create(headingId=self.heading, title='Admin Symptom View title', text='Admin Symptom View text')
        self.sub_heading.ageGroup.add(agegroup)
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_view_page(self):
        """ test the page for the admin_symptom view """
        response = self.client.get(reverse('admin_symptom', kwargs={'symptom_name':self.category.categoryName}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.sub_heading, response.context['results'][0][1])
        self.assertEqual(self.heading, response.context['results'][0][0])
        self.assertTemplateUsed(response, 'admin_symptom.html')

    def test_incorrect_category(self):
        """ test the page for the admin_symptom view with a category that does not exist """
        response = self.client.get(reverse('admin_symptom', kwargs={'symptom_name':'wrong'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin.html')

    def test_category_id(self):
        """ test the page for the admin_symptom view with a category id instead of name """
        response = self.client.get(reverse('admin_symptom', kwargs={'symptom_name':self.category.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_symptom.html')

    def test_incorrect_category_id(self):
        """ test the page for the admin_symptom view with an incorrect category id """
        response = self.client.get(reverse('admin_symptom', kwargs={'symptom_name':'0'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin.html')

class AdminHeadingView(TestCase):
    """ unit test for the admin_headings view """

    def setUp(self):
        Group.objects.create(name='Editors')
        editors_group = Group.objects.get(name='Editors')
        self.admin = User.objects.create_user(username='AdminHeadingViewTest', password='Test', email='email@email.com')
        self.admin.groups.add(editors_group)
        self.client.login(username='AdminHeadingViewTest', password='Test')
        self.category = Category.objects.create(categoryName='AdminHeadingViewTest', description='This is a test for Admin Heading View')
        self.heading = Heading.objects.create(categoryName=self.category, text='This is a test for Admin Heading View')
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_view_page_new_heading(self):
        """ test the page for the admin_headings view with a new heading form"""
        response = self.client.get(reverse('admin_headings', kwargs={'heading_id':'0'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_heading.html')
        self.assertEqual(response.context['form'].as_p(), HeadingEditForm().as_p())

    def test_view_page_heading_exist(self):
        """ test the page for the admin_headings view with a exisiting heading form"""
        response = self.client.get(reverse('admin_headings', kwargs={'heading_id':self.heading.headingId}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_heading.html')
        self.assertEqual(response.context['form'].as_p(), HeadingEditForm(instance=self.heading).as_p())

    def test_add_heading(self):
        """ test adding a new heading """
        response = self.client.post(reverse('admin_headings', kwargs={'heading_id':'0'}), \
        {'categoryName':self.category.pk, 'text':'New Heading'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_symptom.html')
        new_heading = Heading.objects.get(text='New Heading')
        self.assertIn(new_heading, [result[0] for result in response.context['results']])

    def test_edit_existing_heading(self):
        """ test deleteing a heading """
        response = self.client.post(reverse('admin_headings', kwargs={'heading_id':self.heading.headingId}), \
        {'categoryName':self.heading.categoryName.pk, 'text':'Edited Heading'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_symptom.html')
        edited_heading = Heading.objects.get(headingId=self.heading.pk)
        self.assertRaises(Heading.DoesNotExist, Heading.objects.get, text=self.heading.text)
        self.assertEqual(edited_heading.text, 'Edited Heading')
        self.assertNotEqual(edited_heading.text, self.heading.text)
        self.assertIn(edited_heading, [result[0] for result in response.context['results']])
        self.assertNotIn(self.heading.text, [result[0].text for result in response.context['results']])

    def test_delete_heading(self):
        """ test editing a heading which already exists and does not create a new object """
        new_heading = Heading.objects.create(categoryName=self.category, text='Heading to be deleted')
        response = self.client.post(reverse('admin_headings', kwargs={'heading_id':new_heading.headingId}), {'delete':'', \
        'categoryName':new_heading.categoryName.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_symptom.html')
        self.assertRaises(Heading.DoesNotExist, Heading.objects.get, headingId=new_heading.headingId)
        self.assertNotIn(new_heading, [result[0] for result in response.context['results']])

class AdminSubHeadingView(TestCase):
    """ unit test for the admin_subheadings view """

    def setUp(self):
        Group.objects.create(name='Editors')
        editors_group = Group.objects.get(name='Editors')
        self.agegroup = AgeGroup.objects.create(age_group=0)
        self.admin = User.objects.create_user(username='AdminSubHeadingViewTest', password='Test', email='email@email.com')
        self.admin.groups.add(editors_group)
        self.client.login(username='AdminSubHeadingViewTest', password='Test')
        self.category = Category.objects.create(categoryName='AdminSubHeadingViewTest', description='This is a test for Admin SubHeading View')
        self.heading = Heading.objects.create(categoryName=self.category, text='This is a test for Admin SubHeading View')
        self.sub_heading = SubHeading.objects.create(headingId=self.heading, title='Admin SubHeading View title', text='Admin SubHeading View text')
        self.sub_heading.ageGroup.add(self.agegroup)
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_view_page_new_subheading(self):
        """ test the page for the admin_subheadings view with a new sub heading form"""
        response = self.client.get(reverse('admin_subheadings', kwargs={'heading_id':self.heading.pk, 'sub_heading_id':'0'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_subheading.html')
        self.assertEqual(response.context['form'].as_p(), SubHeadingEditForm(initial={'headingId':self.heading.headingId}).as_p())
        self.assertTrue(response.context['new_sub_heading'])

    def test_view_page_subheading_exist(self):
        """ test the page for the admin_subheadings view with a exisiting sub heading form"""
        response = self.client.get(reverse('admin_subheadings', kwargs={'heading_id':self.heading.pk, 'sub_heading_id':self.sub_heading.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_subheading.html')
        self.assertEqual(response.context['form'].as_p(), SubHeadingEditForm(instance=self.sub_heading).as_p())
        self.assertFalse(response.context['new_sub_heading'])

    def test_add_subheading(self):
        """ test adding a new heading """
        response = self.client.post(reverse('admin_subheadings', kwargs={'heading_id':self.heading.pk, 'sub_heading_id':'0'}), \
        {'headingId':self.heading.pk, 'title':'New Sub Heading', 'text':'Text for new sub heading', 'ageGroup':[self.agegroup.pk]}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_symptom.html')
        new_subheading = SubHeading.objects.get(title='New Sub Heading')
        sub_headings = [subheading for subheadings in [result[1] for result in response.context['results']] for subheading in subheadings]
        self.assertIn(new_subheading, sub_headings)

    def test_edit_existing_heading(self):
        """ test deleteing a heading """
        response = self.client.post(reverse('admin_subheadings', kwargs={'heading_id':self.heading.pk, 'sub_heading_id':self.sub_heading.pk}), \
        {'headingId':self.heading.pk, 'title':'Edited Sub Heading', 'text':'Text for new sub heading', 'ageGroup':[self.agegroup.pk]}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_symptom.html')
        edited_subheading = SubHeading.objects.get(subHeadingId=self.sub_heading.pk)
        self.assertRaises(SubHeading.DoesNotExist, SubHeading.objects.get, text=self.sub_heading.title)
        self.assertEqual(edited_subheading.title, 'Edited Sub Heading')
        self.assertNotEqual(edited_subheading.title, self.sub_heading.title)
        sub_headings = [subheading for subheadings in [result[1] for result in response.context['results']] for subheading in subheadings]
        self.assertIn(edited_subheading, sub_headings)

    def test_delete_heading(self):
        """ test editing a heading which already exists and does not create a new object """
        new_subheading = SubHeading.objects.create(headingId=self.heading, title='Admin SubHeading', text='Admin SubHeading to be deleted')
        response = self.client.post(reverse('admin_subheadings', kwargs={'heading_id':self.heading.pk, 'sub_heading_id':new_subheading.pk}), \
        {'delete':''}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_symptom.html')
        self.assertRaises(SubHeading.DoesNotExist, SubHeading.objects.get, subHeadingId=new_subheading.subHeadingId)
        sub_headings = [subheading for subheadings in [result[1] for result in response.context['results']] for subheading in subheadings]
        self.assertNotIn(new_subheading, sub_headings)

class AllURLView(TestCase):
    """ unit test for the all_urls view """

    def setUp(self):
        Group.objects.create(name='Editors')
        editors_group = Group.objects.get(name='Editors')
        self.agegroup = AgeGroup.objects.create(age_group=0)
        self.admin = User.objects.create_user(username='AllURLViewTest', password='Test', email='email@email.com')
        self.admin.groups.add(editors_group)
        self.client.login(username='AllURLViewTest', password='Test')
        self.category = Category.objects.create(categoryName='AllURLViewTest', description='This is a test for All URL View')
        self.heading = Heading.objects.create(categoryName=self.category, text='This is a test for All URL View')
        self.sub_heading = SubHeading.objects.create(headingId=self.heading, title='All URL View title', text='All URL View text')
        self.sub_heading.ageGroup.add(self.agegroup)
        session = self.client.session
        session['disclaimer'] = True
        session.save()

    def test_get_url(self):
        """ test that we get the corect JSON response from the view """
        expected_response = []
        expected_response.append({'name':'Symptom: ' + str(self.category), 'url':self.category.get_absolute_url()})
        expected_response.append({'name':'Heading: ' + str(self.heading), 'url':self.heading.get_absolute_url()})
        expected_response.append({'name':'Sub Heading: ' + str(self.sub_heading), 'url':self.sub_heading.get_absolute_url()})
        response = self.client.get(reverse('all_urls'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_response)
