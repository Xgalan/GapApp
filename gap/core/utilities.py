from django.core.exceptions import ImproperlyConfigured



def get_secret(setting, secrets=None):
    """ Get the secret variable of return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

