from ..middlewares.i18n import gettext, lazy_gettext

fake_gettext = lambda word: word
fake_gettext_plural = lambda word_s, word_p: (word_s, word_p)
