from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        role = data.get('role')
        user.role = role
        return super().save_user(request, user, form, commit)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
