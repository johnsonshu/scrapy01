# use environment variable to switch profile
SCRAPY_SETTINGS_MODULE

https://www.programcreek.com/python/example/102894/scrapy.settings.Settings

# don't forget adding index for mongodb text search

```
db.sites.ensureIndex({title:"text",url:"text"}, {default_language: "none", language_override: "none"} ))
```

# scrapyd config in ubuntu20-lts use ~/.scrapyd.conf
https://scrapyd.readthedocs.io/en/stable/config.html

# scrapyd has been installed as a service:
https://stackoverflow.com/questions/47065225/preferred-way-to-run-scrapyd-in-the-background-as-a-service

# run spider example:
curl http://ubuntu20-lts:6800/schedule.json -d project=scrapy01 -d spider=yifymovies

# confirm selenium version
>>> import selenium    
>>> help (selenium)


# setuptools find_packages returns empty list
https://stackoverflow.com/questions/64404003/setuptools-find-packages-returns-empty-list
find_packages internally searchs for __init__.py under the directories/folders
Create an empty __init__.py then re run find_packages

# TODO: need to gracefully close the selenium web driver.