from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        # Get the user instance but don't save to the database yet
        user = super().save(commit=False)
        
        # Force the username to be the exact same as the email they entered
        user.username = user.email 
        
        # Now save to the database safely
        if commit:
            user.save()
        return user