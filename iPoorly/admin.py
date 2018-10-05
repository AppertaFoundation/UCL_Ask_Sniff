# pylint: disable=R0201
""" model settings for the django admin page """
from django.contrib import admin
from .models import Child, Heading, SubHeading, Category, AgeGroup, DiaryLog


class ChildAdmin(admin.ModelAdmin):
    """ the admin page view and settings for the Child model """
    model = Child
    list_display = ['id', 'get_username', 'childName', 'dob', 'activate']

    def get_username(self, obj):
        """ get username of the object to display in records table """
        return obj.username.username

    get_username.admin_order_field = 'username'
    get_username.short_description = 'Username'

class HeadingInline(admin.StackedInline):
    """ Used to add Heading objects in the Category admin page """
    model = Heading


class SubHeadingInline(admin.TabularInline):
    """ Used to add SubHeading objects in the Heading admin page """
    model = SubHeading

class CategoryAdmin(admin.ModelAdmin):
    """ the admin page view and settings for the Category model """
    model = Category
    list_display = ['categoryId', 'categoryName', 'description']
    inlines = [HeadingInline]

class HeadingAdmin(admin.ModelAdmin):
    """ the admin page view and settings for the Heading model """
    model = Heading
    list_display = ['headingId', 'get_category', 'text']

    def get_category(self, obj):
        """ get category name of the object to display in records table """
        return obj.categoryName.categoryName

    get_category.admin_order_field = 'categoryName'
    get_category.short_description = 'Category'

    inlines = [SubHeadingInline]

class SubHeadingAdmin(admin.ModelAdmin):
    """ the admin page view and settings for the SubHeading model """
    list_display = ['subHeadingId', 'get_heading', 'title', 'text', 'get_age_group', 'lastEdited']

    def get_heading(self, obj):
        """ get heading text of the object to display in records table """
        return obj.headingId.text
    def get_age_group(self, obj):
        """ return list of age groups for the subheading """
        return ", ".join([str(x) for x in obj.ageGroup.all()])

    get_heading.admin_order_field = 'headingId'
    get_heading.short_description = 'Heading Text'
    get_age_group.short_description = 'Age Groups'

class AgeGroupAdmin(admin.ModelAdmin):
    """ the admin page view and settings for the AgeGroup model """
    list_display = ['age_group']

class DiaryLogAdmin(admin.ModelAdmin):
    """ the admin page view and settings for the DiaryLog model """
    list_display = ['diary_id', 'get_child', 'title', 'text', 'image', 'created_on']

    def get_child(self, obj):
        """ get username of the object to display in records table """
        return obj.child.childName

    get_child.admin_order_field = 'child'
    get_child.short_description = 'Child Name'



admin.site.register(Child, ChildAdmin)
admin.site.register(Heading, HeadingAdmin)
admin.site.register(SubHeading, SubHeadingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AgeGroup, AgeGroupAdmin)
admin.site.register(DiaryLog, DiaryLogAdmin)
