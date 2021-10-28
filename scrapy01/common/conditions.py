import re

from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.by import By

def carousel_done():
    """wait for all links rendered : owlCarousel({items:4, lazyLoad:!0 ... )"""   
    def _predicate(driver):
        # firstPhase = driver.page_source
        # cntRe = re.compile(r'\.owlCarousel\({items:(\d+)\),')
        # cnt = cntRe.match(firstPhase).group[0]
        # if cnt == None :
        #     return False
        pageLoaded = (driver.execute_script("return document.readyState") == "complete")
        cntRendered = len( driver.find_elements(By.XPATH,'//div[@class="owl-item"]//img') )

        return pageLoaded and ( cntRendered > 0 )
    return _predicate