# admin_panel/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class StaffRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure the user is logged in and is a staff member.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        if not self.request.user.is_authenticated:
             return redirect('accounts:login') # Redirect to login if not logged in
        else:
             return redirect('home') # Redirect home if logged in but not staff