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

class Academic(models.Model):
    SCHOOL_CHOICES = [
        ("primary", "Primary School"),
        ("secondary", "Secondary School"),
    ]

    school = models.CharField(
        max_length=20,
        choices=SCHOOL_CHOICES,
        unique=True,
        help_text="Primary or Secondary"
    )

    description = models.TextField(
        help_text="Main description about this school level"
    )

    image = models.ImageField(
        upload_to="academics/",
        blank=True,
        null=True,
        help_text="Image for this section"
    )

    quote = models.TextField(
        blank=True,
        help_text="Optional quote"
    )

    teacher_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Name of the teacher/head"
    )

    teacher_designation = models.CharField(
        max_length=150,
        blank=True,
        help_text="Designation of the teacher (e.g. Head of Primary)"
    )

    class Meta:
        verbose_name = "Academic Section"
        verbose_name_plural = "Academic Sections"
        ordering = ["school"]

    def __str__(self):
        return self.get_school_display()


class ContactInfo(models.Model):
    telephone = models.TextField(
        help_text="You can add multiple numbers. Separate them with a comma or new line."
    )

    email = models.EmailField(
        help_text="Main contact email address"
    )

    facebook_link = models.URLField(
        blank=True,
        null=True,
        help_text="Full Facebook page URL"
    )

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "School Contact Information"

    def get_telephone_list(self):
        if not self.telephone:
            return []
        numbers = self.telephone.replace(",", "\n").splitlines()
        return [num.strip() for num in numbers if num.strip()]

class YearlyResult(models.Model):
    year = models.PositiveIntegerField(unique=True)
    candidates = models.PositiveIntegerField()
    pass_rate = models.DecimalField(max_digits=5, decimal_places=2)
    average = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return f"Result {self.year}"

class Topper(models.Model):
    name = models.CharField(max_length=150)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to="toppers/", blank=True, null=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.name} - {self.score}"

class GalleryEvent(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.CharField()

    class Meta:
        ordering = ["-id"]
        verbose_name = "Gallery Event"
        verbose_name_plural = "Gallery Events"

    def __str__(self):
        return f"{self.event_name} ({self.event_date})"

class GalleryImage(models.Model):
    event = models.ForeignKey(
        GalleryEvent,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="gallery/")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Image for {self.event.event_name}"