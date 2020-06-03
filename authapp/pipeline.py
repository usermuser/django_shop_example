from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from django.http import HttpResponse

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https', 'api.vk.com', '/method/users.get', None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                    access_token=response['access_token'],
                                                    v='5.92')), None
                            ))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        print(data)
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.aboutMe = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            # TODO
            # месяц тоже нужно учитывать, при этом учитывать страну
            # так как в некоторых странах первым идет месяц затем день 12.24.1985 - 24 декабря
            # если включить зануду, то и день нужно проверять :)
            # вроде как страну не всегда можно узнать, значит принимаем по дефолтку дд.мм.гг.
            age = timezone.now().date().year - bdate.year

            if age < 1800:
                user.delete()

                # raise AuthForbidden('social_core.backends.vk.VKOAuth2')
                error_msg = AuthForbidden("social_core.backends.vk.VKOAuth2")
                person = data["first_name"]

                return HttpResponse(f'<h3>Dear {person}:</h3>'
                                    f'<h4>{error_msg}</h4>')

            else:  # явное лучше неявного
                user.age = age

        user.save()

    elif backend.name == 'google-oauth2':
        pass

    return