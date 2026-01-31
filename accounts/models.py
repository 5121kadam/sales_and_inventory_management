from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import AutoSlugField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField

# define choices fro profile status and roles
STATUS_CHOICES = [
    ('INA', 'Inactive'),
    ('A', 'Active'),
    ('OL', 'On Leave')
]

ROLE_CHOICES = [
    ('OP', 'Operator'),
    ('EX', 'Executive'),
    ('AD', 'Admin')
]

class Profile(models.Model):
    """
    Represents a user profile containing personal and account-related information.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='User'
    )

    slug = AutoSlugField(
        unique=True,
        verbose_name='Account ID',
        populate_from='email'
    )

    display_name=models.ImageField(
        upload_to='profile_pics',
        default='profile_pics/cat.2.jpg',
        null=True,
        blank=True
    )

    telephone = PhoneNumberField(
        null=True, blank=True, verbose_name='Telephone'
    )

    email = models.EmailField(
        max_length=150, blank=True, null=True, verbose_name='Email'
    )

    first_name = models.CharField(
        max_length=30, blank=True, verbose_name='First Name'
    )

    last_name = models.CharField(
        max_length=30, blank=True, verbose_name='Last Name'
    )    

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=12,
        default='INA',
        verbose_name='Status'
    )

    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=12,
        blank=True,
        null=True,
        verbose_name='Role'
    )

    def image_url(self):
        """
        Retruns the URL of the profile picture.
        Returns aN empty string if the image is not available
        """
        try:
            return self.profile_picture.url
        except AttributeError:
            return ''
    
    def __str__(self):
        """
        Returns a string representation of the profile
        """
        return f"{self.user.username} profile"
    
    class Meta:
        """Meta options of the profile model."""
        ordering = ['slug']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Vendor(models.Model):
    """
    Represents a vendor with contact and address information.
    """

    name = models.CharField(max_length=50, verbose_name='Name')
    slug = AutoSlugField(
        unique=True,
        populate_from='name',
        verbose_name='Slug'
    )

    phone_number = models.BigIntegerField(
        blank=True, null=True, verbose_name='Phone Number'
    )

    address = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Address'
    )

    def __str__(self):
        """ Return a string represntation of the vendor"""

        return self.name
    
    class Meta:
        """Meta options for the Vendor Model."""
        Verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

class Customer(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    address = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null= True)
    loyalty_profile = models.IntegerField(default=0)

    class Meta:
        db_table = 'Customers'

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def to_select2(self):
        item = {
            "label": self.get_full_name(),
            "value": self.id
        }
        return item


