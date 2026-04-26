# api/forms.py
from django import forms
from .models import Organization

class CustomSignupForm(forms.Form):
    # 1. Define the mandatory field. 'required=True' ensures the API blocks 
    # the request if the frontend forgets to send it.
    organization_name = forms.CharField(max_length=255, required=True, strip=True)

    def signup(self, request, user):
        """
        Allauth built in hook.Runs immediately 
        after the User object is created.
        """
        # Get the validated organization name from the JSON request
        org_name = self.cleaned_data['organization_name']
        
        # 2. Create the brand new Organization with the user's chosen name
        new_org = Organization.objects.create(name=org_name)

        # 3. Attach the organization to the user and upgrade their role
        user.organization = new_org
        user.role = 'ADMIN'
        
        # 4. Save the final user state
        user.save()