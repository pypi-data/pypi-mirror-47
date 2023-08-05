# datadog-http-handler

Python logging module allowing you to log directly to Datadog via https.
Currently support only for python 3.6+.

## Installation

Install [python](https://www.python.org/downloads/)

Install [pip](https://pip.pypa.io/en/stable/installing/)
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

Install datadog-http-handler
```bash
pip install datadog-http-handler
```

## Usage

The typical usage of this library to output to datadog

```bash
from datadog_http_handler import DatadogHttpHandler

logger = DatadogHttpHandler(
    api_key=os.getenv('DATADOG_API_KEY', ''),
    service='test',
    host='your_hostname',
    logger_name='example',
    tags={'env': 'test', 'user': 'Tim the Enchanter'}
).logger

logger.info('Hello World')
```

Since sending logs to datadog via http can issue in a request failure for a myriad of reasons, it would be
good to know if the failure accord.  By setting raise_failure=True when creating the DatadogHttpHandler
object, an exception will now be thrown if the status code of the response is not 200.  See below:

```bash
import traceback

from datadog_http_handler import DatadogHttpHandler

logger = DatadogHttpHandler(
    api_key=os.getenv('DATADOG_API_KEY', ''),
    raise_exception=True,
    service='test',
    host='your_hostname',
    logger_name='example',
    tags={'env': 'test', 'user': 'Tim the Enchanter'}
).logger

try:
    logger.info('Hello World')
exceptException as e:
    print(traceback.format_exc())
```

## LICENSE

[MIT](https://github.com/nrccua/datadog-http-handler/blob/master/LICENSE)

## AUTHORS

* **NRCCUA Software Engineers**

See also the list of [contributors](https://github.com/nrccua/datadog-http-handler/contributors) who participated in this project.

## ACKNOWLEDGEMENTS

* **Bryan Cusatis** - NRCCUA Architecture Team Lead
* **Tim Reichard** - NRCCUA Architecture Team Member
* **Grant Evans** - NRCCUA DevOps Engineering Lead
