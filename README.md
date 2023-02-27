# payhere-assignment

Payment 백엔드 포지션 과제입니다

- [요구사항](https://github.com/gghotted/payhere-assignment/issues/1)
- 2023-02-24 ~ 2023-02-27 동안 진행되었습니다.

<br/>

## API

상세 스팩은 [swagger hub](https://app.swaggerhub.com/apis-docs/gghotted/payhere-assignment/1.0.0)에 정의하였습니다.

### Endpoint 설계

- 가독성을 위해 최대한 상위 리소스 정보를 포함하였습니다.
  - 너무 길어질 경우 적절히 생략하였습니다.

### Response 룰

- 일반적인 리소스 생성의 경우 `id`, `created_at` 정보를 응답합니다.
- 리소스 수정의 경우 리소스 디테일 api의 응답과 같습니다.

### 인증 방식

- jwt 방식을 사용하며, header에 `Authorization: Bearer {access_token}`을 넣어 인증합니다.
- 일부 api(가계부-거래내역 상세)의 경우 query에 `guest={guest_code}`를 넣어 일시적으로 접근 가능합니다.

<br/>

## 구현

- 테스트 코드를 작성하여 작성된 코드의 안정성과 수정을 용이하도록 하였습니다.
- Mixin과 상속을 통해 재사용성을 늘리고자 노력하였습니다.
  - [CopyView](https://github.com/gghotted/payhere-assignment/blob/1689593b1399156e284cdff63781dcfb8bd0d22c/apps/core/views.py#L21)
  - [ShareLinkCreateAPIView](https://github.com/gghotted/payhere-assignment/blob/1689593b1399156e284cdff63781dcfb8bd0d22c/apps/share/views.py#L70)
  - ...
- 확장성을 고려하여 share기능을 만들었습니다.
  - 공유된 링크(front page)에서 여러 api에 접근하는 상황을 고려하였습니다.
  - 기존에 작성된 View에 [IsGuest](https://github.com/gghotted/payhere-assignment/blob/1689593b1399156e284cdff63781dcfb8bd0d22c/apps/share/permissions.py#L7) 퍼미션을 추가하는 방식입니다.([사용 예시](https://github.com/gghotted/payhere-assignment/blob/1689593b1399156e284cdff63781dcfb8bd0d22c/apps/account_books/views.py#L76))
    - `access_scode`값을 활용하여, api 접근 범위를 제한하였습니다.
  - 이 기능의 방식은 [django-sesame](https://github.com/aaugustin/django-sesame)을 참고하였습니다.
    - 이 패키지는 공유 토큰마다 만료 시간을 다르게 설정하기 힘든 점, 강제로 만료시킬 수 없는 점이 아쉬워서 사용하지 않았습니다.

### 주요 사용 패키지

- [django](https://github.com/django/django), [django-rest-framework](https://github.com/encode/django-rest-framework), [djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt)
- [freezegun](https://github.com/spulec/freezegun)
  - 만료일을 테스트하기위해 사용하였습니다.
- [django-extensions](https://github.com/django-extensions/django-extensions)
  - `guest_code`를 저장하기 위해 `RandomCharField`을 사용하였습니다.

<br/>

## 실행 방법

### Product(docker-compose)

```bash
git clone https://github.com/gghotted/payhere-assignment
cd payhere-assignment
docker-compose --env-file .env build
docker-compose --env-file .env up
```

- 과제인 점을 감안하여, 설정 파일을 같이 푸시하였습니다.

### Local

```bash
git clone https://github.com/gghotted/payhere-assignment
cd payhere-assignment/
virtualenv venv
pip install -r requirements.txt

cd apps
python manage.py migrate
python manage.py runserver

# 테스트 실행
python manage.py test core.fixtures
python manage.py test
```

