# import pytest
# from django.conf import settings
# import dj_database_url
#
# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES = {
#         'default': dj_database_url.config(
#             default="postgres://max:Anykey@localhost/flowershop_db",
#         )
#     }