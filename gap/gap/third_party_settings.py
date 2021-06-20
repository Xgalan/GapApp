# third party/libraries configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
