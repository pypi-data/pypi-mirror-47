# Convert value from usd to currency

Simple and free usd2currency convert utils,
by caching free-limited-api from apilayer.com

## Quick start

1. Install::

``` 
   pip install django-usd2currency
```

1. Add "django_usd2currency" to your INSTALLED_APPS setting like this::

```
   INSTALLED_APPS = [
   ...
   'django_usd2currency',
   ]
   # Get free api from https://currencylayer.com/signup/free
   APILAYER_ACCESS_KEY = 'xxxxxxxxxxx'
```

1. Start to use it in code

```
   from django_usd2currency.utils import usd2currency

   print(usd2currency(12, currency='CNY'))
```

1. Use [redis as cache backend](https://niwinz.github.io/django-redis/latest/) to lock in the multiprocess env.


## TODO:

* write test
