# RESTArt-Falcon

A RESTArt extension for integrating [RESTArt][1] into [Falcon][2], which has the benefit of high performance.


## Why

**Pros**: With `RESTArt-Falcon`, you can benefit from the high performance of Falcon, while still using the RESTArt-style API code, which I think is more Pythonic.

**Cons**: The Werkzeug-style converters (with the separator `:`) is not supported in `RESTArt-Falcon`. Captured parameters in URI can only be specified in the form of `<arg>`, which will be automatically converted to Falcon-style `{arg}`.


## Benchmarks

### Codebase

Pure `RESTArt` API:

```python
from restart.api import RESTArt
from restart.resource import Resource
from restart.serving import Service

api = RESTArt()

@api.route(method=['GET'])
class Action(Resource):
    name = 'action'

    def read(self, request):
        return 'Go'

app = Service(api)
```

`RESTArt-Falcon` API:

```python
from restart.api import RESTArt
from restart.resource import Resource
from restart.serving import Service
from restart.ext.falcon.adapter import FalconAdapter

api = RESTArt()

@api.route(method=['GET'])
class Action(Resource):
    name = 'action'

    def read(self, request):
        return 'Go'

app = Service(api, FalconAdapter)
```

`Falcon` API:

```python
import falcon

class Action(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'Go'

app = falcon.API()
app.add_route('/action', Action())
```

### Scenario

OS           | CPU     | Memory | Gunicorn  | Benchmark Command
------------ | ------- | ------ | --------- | ---------------------------------
Ubuntu 14.04 | 4 cores | 8 G    | 8 workers | [http_load][3] -p 100 -s 10 [url_file]

### Result

Framework (or Library) | reqs/s | us/req
---------------------- | ------ | ------
RESTArt                | 2893   | 345
RESTArt-Falcon         | 4020   | 248
Falcon                 | 6310   | 158


[1]: https://github.com/RussellLuo/restart
[2]: https://github.com/falconry/falcon
[3]: http://www.acme.com/software/http_load/
