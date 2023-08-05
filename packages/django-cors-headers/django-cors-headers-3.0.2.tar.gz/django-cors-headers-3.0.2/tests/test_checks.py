from __future__ import absolute_import

import re

import pytest
from django.core.checks import Error
from django.core.management import base, call_command
from django.test import SimpleTestCase
from django.test.utils import override_settings

from corsheaders.checks import check_settings


class ChecksTests(SimpleTestCase):

    def check_error_codes(self, expected):
        errors = check_settings([])
        assert len(errors) == len(expected)
        assert all(isinstance(e, Error) for e in errors)
        assert [e.id for e in errors] == expected

    def test_defaults_pass(self):
        self.check_error_codes([])

    def test_defaults_pass_check(self):
        call_command('check')

    @override_settings(CORS_ORIGIN_ALLOW_ALL=object)
    def test_checks_are_bound(self):
        with pytest.raises(base.SystemCheckError):
            call_command('check')

    @override_settings(CORS_ALLOW_HEADERS=object)
    def test_cors_allow_headers_non_sequence(self):
        self.check_error_codes(['corsheaders.E001'])

    @override_settings(CORS_ALLOW_HEADERS=[object])
    def test_cors_allow_headers_non_string(self):
        self.check_error_codes(['corsheaders.E001'])

    @override_settings(CORS_ALLOW_METHODS=object)
    def test_cors_allow_methods_non_sequence(self):
        self.check_error_codes(['corsheaders.E002'])

    @override_settings(CORS_ALLOW_METHODS=[object])
    def test_cors_allow_methods_non_string(self):
        self.check_error_codes(['corsheaders.E002'])

    @override_settings(CORS_ALLOW_CREDENTIALS=object)
    def test_cors_allow_credentials_non_bool(self):
        self.check_error_codes(['corsheaders.E003'])

    @override_settings(CORS_PREFLIGHT_MAX_AGE='10')
    def test_cors_preflight_max_age_non_integer(self):
        self.check_error_codes(['corsheaders.E004'])

    @override_settings(CORS_PREFLIGHT_MAX_AGE=-1)
    def test_cors_preflight_max_age_negative(self):
        self.check_error_codes(['corsheaders.E004'])

    @override_settings(CORS_ORIGIN_ALLOW_ALL=object)
    def test_cors_origin_allow_all_non_bool(self):
        self.check_error_codes(['corsheaders.E005'])

    @override_settings(CORS_ORIGIN_WHITELIST=object)
    def test_cors_origin_whitelist_non_sequence(self):
        self.check_error_codes(['corsheaders.E006'])

    @override_settings(CORS_ORIGIN_WHITELIST=[object])
    def test_cors_origin_whitelist_non_string(self):
        self.check_error_codes(['corsheaders.E006'])

    @override_settings(CORS_ORIGIN_WHITELIST=['http://example.com', 'null'])
    def test_cors_origin_whitelist_allowed(self):
        self.check_error_codes([])

    @override_settings(CORS_ORIGIN_WHITELIST=['example.com'])
    def test_cors_origin_whitelist_no_scheme(self):
        self.check_error_codes(['corsheaders.E013'])

    @override_settings(CORS_ORIGIN_WHITELIST=['https://'])
    def test_cors_origin_whitelist_no_netloc(self):
        self.check_error_codes(['corsheaders.E013'])

    @override_settings(CORS_ORIGIN_WHITELIST=['https://example.com/foobar'])
    def test_cors_origin_whitelist_path(self):
        self.check_error_codes(['corsheaders.E014'])

    @override_settings(CORS_ORIGIN_REGEX_WHITELIST=object)
    def test_cors_origin_regex_whitelist_non_sequence(self):
        self.check_error_codes(['corsheaders.E007'])

    @override_settings(CORS_ORIGIN_REGEX_WHITELIST=[re.compile(r'a')])
    def test_cors_origin_regex_whitelist_regex(self):
        self.check_error_codes([])

    @override_settings(CORS_EXPOSE_HEADERS=object)
    def test_cors_expose_headers_non_sequence(self):
        self.check_error_codes(['corsheaders.E008'])

    @override_settings(CORS_EXPOSE_HEADERS=[object])
    def test_cors_expose_headers_non_string(self):
        self.check_error_codes(['corsheaders.E008'])

    @override_settings(CORS_URLS_REGEX=object)
    def test_cors_urls_regex_non_string(self):
        self.check_error_codes(['corsheaders.E009'])

    @override_settings(CORS_REPLACE_HTTPS_REFERER=object)
    def test_cors_replace_https_referer_failure(self):
        self.check_error_codes(['corsheaders.E011'])

    @override_settings(CORS_MODEL='something')
    def test_cors_model_failure(self):
        self.check_error_codes(['corsheaders.E012'])
