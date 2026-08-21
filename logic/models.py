from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, name, password=None):
        if not name:
            raise ValueError("Users must have a name")
        user = self.model(name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None):
        user = self.create_user(name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=150, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class AboutSection(models.Model):
    SECTION_CHOICES = [
        ("history", "Our History"),
        ("principal", "Message from the Principal"),
        ("chairperson", "Message from the Chairperson"),
    ]

    section = models.CharField(
        max_length=20,
        choices=SECTION_CHOICES,
        unique=True,
        help_text="Which section this content belongs to"
    )

    heading = models.CharField(
        max_length=255,
        blank=True,
        help_text="Main heading or the quote"
    )

    text = models.TextField(
        help_text="The main body text / paragraphs"
    )

    image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True,
        help_text="Optional image for this section"
    )

    person_name = models.CharField(max_length=100, blank=True)
    person_title = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"

    def __str__(self):
        return self.get_section_display()