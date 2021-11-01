# use environment variable to switch profile
SCRAPY_SETTINGS_MODULE

https://www.programcreek.com/python/example/102894/scrapy.settings.Settings

# don't forget adding index for mongodb text search

```
db.sites.ensureIndex({title:"text",url:"text"}, {default_language: "none", language_override: "none"} ))
```