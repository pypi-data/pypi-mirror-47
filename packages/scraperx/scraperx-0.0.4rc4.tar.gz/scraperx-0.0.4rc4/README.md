# ScraperX  SDK


### Getting Started

1. Create a new directory where the scraper will live and add the following files:
    - A config file: `config.yaml` [(Example)](./examples/config.yaml)
    - The scraper file: `your_scraper.py` [(Example)](./examples/minimal.py)
1. Next install this library from pypi: `pip install scraperx`
1. Run the full scraper by running `python your_scraper.py dispatch`
    - To see the arguments for the command: `python your_scraper.py dispatch -h`
    - See all the commands available: `python your_scraper.py -h`


## Developing

Any time the scraper needs to override the bases `__init__`, always pass in `*args` & `**kwargs` like so:  
```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
```

### Dispatching

#### Task data
This is a dict of values that is passed to each step of the process. The scraper can put anything it wants here that it may need. But here are a few build in values that are not requiored, but are used if you do supply them:

- `headers`: Dict of headers to use each request
- `proxy`: Full proxy string to be used
- `proxy_country`: Used to get a proxy for this region, if this and `proxy` are not set, a random proxy will be used.
- `device_type`: used when setting a user-agent if one was not set. Options are `desktop` or `mobile`

### Downloading

Uses a `requests.Session` to make get and post requests.
The `__init__` of the `BaseDownload` class can take the following args:
- task: Required. The task from the dispatcher
- headers: (Named arg) dict to set headers for the whole session. default: random User-Agent for the device type, will use desktop if no device type is set
- proxy: (Named arg) Proxy string to use for the requests
- ignore_codes: (Named arg) List of HTTP Status codes to not retry on. If these codes are seen, it will treat the request as any other success. 


When using BaseDownloader, a requests session is created under `self.session`, so every get/post you make will use the same session per task.
Headers can also be set per call by pasing the keyword args to self.request_get() and self.request_post(). Any kwargs you pass to self.get/post will be pased to the sessions get/post methods.

When using BaseDownloader's get & post functions, it will use the requests session created in __init__ and a python `requests` response object.

A request will retry _n_ times (3 by default) to get a successful status code, each retry it will try and trigger a function called `new_profile()` where you have the chance to switch the headers/proxy the request is using (will only update for that request?). If that function does not exist, it will try again with the same data.


#### Setting headers/proxies

The ones set in the `self.request_get/request_post` will be combined with the ones set in the `__init__` and override if the key is the same.

self.request_get/request_post kwargs headers/proxy  
will override  
self.task[headers/proxy]  
will override  
__init__ kwargs headers/proxy  

Any header/proxy set on the request (get/post/etc) will only be set for that single request. For those values to be set in the session they must be set from the init or be in the task data.

#### Proxies
If you have a list of proxies that the downloader should auto rotate between they can be saved in a csv in the following format:
```csv
proxy,country
http://user:pass@some-server.com:5500,US
http://user:pass@some-server.com:5501,US
http://user:pass@some-server.com:6501,DE
```
Set the env var `PROXY_FILE` to the path of the above csv for the scraper to load it in.  
If you have not passed in a proxy directly in the task and this proxy csv exists, then it will pull a random proxy from this file. It will use the `proxy_country` if set in the task data to select the correct country to proxy to.

#### User-Agent
If you have `device_type` set in the task data, then a random user-agent for that device type will be used. If `device_type` is not set, it will default to use a desktop user-agent.
To set your own list of user-agents to choose from, create a csv in the following format:  
```csv
device_type,agent
desktop,"Some User Agent for desktop"
desktop,"Another User Agent for desktop"
mobile,"Now one for mobile"
```
Set the env var `UA_FILE` to the path of the above csv for the scraper to load it in.  
If you have not directly set a user-agent, a ramdon one will be pulled from the csv based on the `device_type` in the task data.


### Extracting
Coming to a Readme near you...


### Testing
When updating the extractors there is a chance that it will not work with the previous source files. So having a source and its QA'd data file is useful to test against to verify that data is still extracting correctly.

#### Creating test files
1. Run `python your_scraper.py create-test path_to/metadata_source_file`
    - The input file is the `*_metadata.json` file that gets created when you run the scraper and it downloads the source files.
2. This will copy the metadata file and the sources into the directory `tests/sample_data/your_scraper/` using the time the source was downloaded (from the metadata) as the file name.
    - It also creates extracted qa files for each of the sources based on your extractors.
3. The QA files it created will have `_extracted_(qa)_` in the file name. What you have to do it confirm that all values are correct in that file. If everything looks good then fix the file name from having `_extracted_(qa)_` to `_extracted_qa_`. Tjis will let the system know that the file has been checked ans that is the data it will use to compare when testing.
4. Next is to create the code that will run the tests. Create the file `tests/tests.py` with the contents below
```python
import unittest  # The testingframe work to use
from scraperx.test import ExtractorBaseTest  # Does all the heavy lifting for the test
from your_scraper import Extract as YourScraperExtract  # Your scrapers extract class
# If you have multiple scrapers, then import their extract classes here as well


# This test will loop through all the test files for the scraper
class YourScraper(ExtractorBaseTest.TestCase):

    def __init__(self, *args, **kwargs):
        # The directory that the test files for your scraper are in
        data_dir = 'tests/sample_data/your_scraper'
        super().__init__(data_dir, YourScraperExtract, *args, **kwargs)

# If you have multiple scrapers, then create a class for each

# Feel free to include any other unit tests you may want to run as well
```
5. Running the tests `python -m unittest discover -vv`


## Config

3 Ways of setting config values:
- CLI Argument: Will override any other type of config value. Use `-h` to see available options
- Environment variable: Will override a config value in the yaml
- Yaml file: Will use these values if no other way is set for a key

### Config values

```yaml
# config.yaml
# This is a config file with all config values
# Required fields are marked as such

default:
  extractor:
    save_data:
      service: local  # (local, s3) Default: local
      bucket_name: my-extracted-data  # Required if `service` is s3, if local this is not needed
    file_template: test_output/{scraper_name}/{id}_extracted.json  # Optional, Default is "output/source.html"

  downloader:
    save_data:
      service: local  # (local, s3) Default: local
      bucket_name: my-downloaded-data  # Required if `service` is s3, if local this is not needed
    file_template: test_output/{scraper_name}/{id}_source.html  # Optional, Default is "output/extracted.json"

  dispatch:
    limit: 5  # Default None. Max number of tasks to dispatch. If not set, all tasks will run
    service:
      # This is where both the download and extractor services will run
      name: local  # (local, sns) Default: local
      sns_arn: sns:arn:of:service:to:trigger  # Required if `name` is sns, if local this is not needed
    ratelimit:
      type: qps  # (qps, period) Required. `qps`: Queries per second to dispatch the tasks at. `period`: The time in hours to dispatch all of the tasks in.
      value: 1  # Required. Can be an int or a float. When using period, value is in hours
```

If you are using the `file_template` config, a python `.format()` runs on this string so you can use `{key_name}` to make it dynamic. The keys you will have direct access to are the following:
  - All keys in your task that was dispatched
  - Any thing you pass into the `template_values={}` kwarg for the `.save()` fn
  - `time_downloaded`: time (utc) passed from the downloader (in both the downlaoder and extractor)
  - `date_downloaded`: date (utc) passed from the downloader (in both the downlaoder and extractor)
  - `time_extracted`: time (utc) passed from the extractor (just in the extractor)
  - `date_extracted`: date (utc) passed from the extractor (just in the extractor)

Anything under the `default` section can also have its own value per scraper. So if we have a scraper named `search` and we want it to use a different rate limit then all the other scrapers you can do:
```yaml
# Name of the python file
search:
  dispatch:
    ratelimit:
      type: period
      value: 5
```

To override the `value` in the above snippet using an environment variable, set `DISPATCH_RATELIMIT_VALUE=1`. This will overide all dispatch ratelimit values in default and custom.



### Sample scrapers
Samle scrapers can be found in the [examples](./examples) folder of this repo
