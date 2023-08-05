# Python ISL

A python package to communicate with ISL's api and authenticate ISL employees in Django.

## API

### Installation
```
    pip install python-isl
```

### Usage
```
    from pythonisl import ISLClient

    access_token = os.environ.get('ISL_ACCESS_TOKEN')
    isl_endpoint = os.environ.get('ISL_API_ENDPOINT')

    isl = ISLClient(access_token, isl_endpoint)

    for employee in isl.employees():
        print(employee)
    for team in isl.teams():
        print(team)
    for dog in isl.dogs():
        print(dog)

    print(isl.teams().get('antimatter'))  # this line is the
    print(isl.teams('antimatter').get())  # same as this line
```

## AUTH

### Installation
```
    pip install python-isl
```
### Configuration

in `settings.py`
```
AUTHENTICATION_BACKENDS = (
    'pythonisl.backends.ISLAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
```
in `urls.py`
```
    urlpatters += [url('', include('pythonisl.urls')),]
```
this adds the urls: `login/`, `auth/callback/`, and `logout/`
you can include the individual views if you would like instead
```
    from pythonisl.views import login, callback, logout
```
the `callback` url must be named "islauth_callback"

### Usage

Just point a user to /login/?next=/my-next-url/
The ISLAuthBackend will take care of logging the user in by email address
or creating a new user by email address and the user portion of the email
being the username.

The user will stay logged in as long as the session is still valid, and
you can request that they login by directing them to the /login/ url whenever
you want.
