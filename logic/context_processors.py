from django.core.cache import cache
from .models import ContactInfo

def global_context(request):
    contact = cache.get("site_contact_info")

    if contact is None:
        contact = ContactInfo.objects.first()
        cache.set("site_contact_info", contact, 60 * 15)

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