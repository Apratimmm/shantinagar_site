from django.core.cache import cache
from .models import ContactInfo

CACHE_KEY = "site_contact_info"
CACHE_TTL = 60 * 15

def get_contact_info():
    contact = cache.get(CACHE_KEY)

    if contact is None:
        contact = ContactInfo.objects.first()
        cache.set(CACHE_KEY, contact, CACHE_TTL)

    return contact

def global_context(request):
    contact = get_contact_info()

    if contact:
        return {
            "logo_url": contact.logo.url if contact.logo else None,
            "contact_numbers": contact.get_telephone_list(),
            "email_address": contact.email,
            "facebook_link": contact.facebook_link,
        }

    return {
        "logo_url": None,
        "contact_numbers": [],
        "email_address": None,
        "facebook_link": None,
    }
