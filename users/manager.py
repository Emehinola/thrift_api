from django.contrib.auth.models import BaseUserManager

class CustomManager(BaseUserManager):

    def create_user(self, email, password=None, *args, **kwargs):
        if not email:
            raise ValueError('Email cannot be None')
        if not password:
            raise ValueError('Password cannot be None')
        
        email = self.normalize_email(email=email)
        user = self.model(email=email, *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, *args, **kwargs):
        if not email:
            raise ValueError('Email cannot be None')
        if not password:
            raise ValueError('Password cannot be None')
        
        user = self.create_user(email=email, password=password, *args, **kwargs)

        # set priviledges
        user.is_admin = True
        user.save()

        return user
