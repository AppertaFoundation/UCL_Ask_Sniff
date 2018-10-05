""" Decorators used in views. Used in place of a block of code so that we dont need to
write the same code again and again The decorator is placed on top of the views function where we
would want the code to be applied. e.g @login_required on top of a view checks that
the user is logged in before viewing that view """
from django.shortcuts import redirect

def disclaimer_required(function):
    """ checks if a user has agreed to the disclaimer before getting access to a view """
    def wrap(request, *args, **kwargs):
        """ code for checking the disclaimer required """
        if not request.session.has_key('disclaimer'):
            return redirect('disclaimer')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def age_required(function):
    """ checks if a user has selected an age """
    def wrap(request, *args, **kwargs):
        """ code for checking an age has been selected"""
        if not request.session.has_key('age_range') and not request.user.is_authenticated():
            return redirect('age')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def admin_required(function):
    """ checks if a user has admin rights """
    def wrap(request, *args, **kwargs):
        """ code for checking the admin required """
        if request.user.groups.filter(name='Editors').exists():
            return function(request, *args, **kwargs)
        return redirect('homepage')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
