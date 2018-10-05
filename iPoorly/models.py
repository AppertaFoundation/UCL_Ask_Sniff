""" Database schema for the project """
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from redactor.fields import RedactorField

class Child(models.Model):
    # pylint: disable=C0103
    """ The Child model contains information about a Child """
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    childName = models.CharField(default='noNameProvided', max_length=150)
    dob = models.DateField(default=datetime.now)
    activate = models.BooleanField(default=False)
    def __str__(self):
        return self.childName

    class Meta:
        ordering = ['-dob']

class Category(models.Model):
    """ The Category model contains information about a symptom """
    categoryId = models.AutoField(primary_key=True)
    categoryName = models.CharField(default='', max_length=150, verbose_name=u'Symptom Name')
    description = RedactorField(verbose_name=u'Description/Summary', default='')
    def __str__(self):
        return self.categoryName.replace("_", " ").title()

    def get_absolute_url(self):
        """ return the url for the model """
        return "/symptom/{}".format(self.categoryName)

    def save(self, *args, **kwargs):
        # pylint: disable=W0221, C0103
        self.categoryName = self.categoryName.lower().replace(" ", "_")
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['categoryName']

class Heading(models.Model):
    """ The Heading model has the title of the heading and which category it belongs to """
    headingId = models.AutoField(primary_key=True)
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=u'Symptom')
    text = models.CharField(default='', verbose_name=u'Heading Title', max_length=500)
    def __str__(self):
        return self.text
    def get_absolute_url(self):
        """ return the url for the model """
        return "/symptom/information/{}".format(self.headingId)
    class Meta:
        ordering = ['headingId']

# ageGroup
# 0 ->less than 1 month
# 1 ->1-3 months
# 2 ->3-6 months
# 3 ->6-12 months
# 4 ->12-24 months
# 5 ->2-5 years

class AgeGroup(models.Model):
    """ The age groups available """
    CHOICES = ((0, 'less than 1 month'), (1, '1-3 months'), (2, '3-6 months'), (3, '6-12 months'),\
    (4, '12-24 months'), (5, '2-5 years'))
    age_group = models.IntegerField(default=0, choices=CHOICES, verbose_name=u'Age Group')

    def __str__(self):
        return str(self.get_age_group_display())


class SubHeading(models.Model):
    """ The SubHeading model contains the information for a certain topic of a Heading """
    subHeadingId = models.AutoField(primary_key=True)
    headingId = models.ForeignKey(Heading, on_delete=models.CASCADE, verbose_name=u'Heading')
    title = models.CharField(default='', max_length=150, verbose_name=u'Title')
    text = RedactorField(verbose_name=u'Content')
    ageGroup = models.ManyToManyField(AgeGroup)
    lastEdited = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s (%s)" % (self.title, ", ".join([str(x) for x in self.ageGroup.all()]))
    def get_absolute_url(self):
        """ return the url for the model """
        return "/symptom/information/{}#{}".format(self.headingId.headingId, self.subHeadingId)
    class Meta:
        ordering = ['subHeadingId']

class DiaryLog(models.Model):
    """ The DiaryLog model contains information about each diary logs for a child """
    diary_id = models.AutoField(primary_key=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    title = models.CharField(default='', max_length=150, verbose_name=u'Title')
    text = models.TextField(default='', max_length=2400, verbose_name='Diary Entry')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True)
    class Meta:
        ordering = ['created_on']
          