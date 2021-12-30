# install prerequisites

### install python
https://www.python.org/downloads/

### install scrapy
https://docs.scrapy.org/en/latest/intro/install.html

### install itemloads
https://pypi.org/project/itemloaders/

### install pymongo
https://pypi.org/project/pymongo/

### install selenium and drivers
https://www.geeksforgeeks.org/how-to-install-selenium-in-python/
https://selenium-python.readthedocs.io/installation.html

make sure selenium driver path is in PATH environment variable

### install mongodb
https://docs.mongodb.com/v4.0/installation/

# usage
### scrapy.cfg
in this file, you can select setting you want to use.
Defautl value is scrapy01.settings_dev_with_proxy, because I'm in China mainland.
Don't forget enabling your own proxy and configure the right server and port. 

### command
You can use "scrapy runspider <spider_file.py>." for a single spider.
for example: scrapy runspider scrapy01/spiders/douxing/yifymovies.py

### result sample
data in MongoDB:
![image](readme-files\mongodata01.png)

downloaded files structure:
![image](readme-files\downloaded-files.png)

