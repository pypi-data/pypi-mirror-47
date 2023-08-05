import time
from selenium.webdriver.common.action_chains import ActionChains

from .config import settings
from .common import SELENIUM_EXCEPTIONS, archiver, click_button

# Used as a threshold to avoid running forever
MAX_POSTS = settings["MAX_POSTS"]

def delete_posts(driver,
                 user_profile_url,
                 year=None):
    """
    Deletes or hides all posts from the wall

    Args:
        driver: seleniumrequests.Chrome Driver instance
        user_profile_url: str
        year: optional int YYYY year
    """

    if year is not None:
        user_profile_url = "{0}/timeline?year={1}".format(user_profile_url, year)

    driver.get(user_profile_url)

    for _ in range(MAX_POSTS):
        post_button_sel = "_4xev"

        post_content_sel = "userContent"
        post_timestamp_sel = "timestampContent"

        wall_log, archive_wall_post = archiver("wall")

        while True:
            try:
                timeline_element = driver.find_element_by_class_name(post_button_sel)

                post_content_element = driver.find_element_by_class_name(post_content_sel)
                post_content_ts = driver.find_element_by_class_name(post_timestamp_sel)

                archive_wall_post(post_content_element.text, timestamp=post_content_ts.text)

                actions = ActionChains(driver)
                actions.move_to_element(timeline_element).click().perform()

                menu = driver.find_element_by_css_selector("#globalContainer > div.uiContextualLayerPositioner.uiLayer > div")
                actions.move_to_element(menu).perform()

                try:
                    delete_button = menu.find_element_by_xpath("//a[@data-feed-option-name=\"FeedDeleteOption\"]")
                except SELENIUM_EXCEPTIONS:
                    try:
                        delete_button = menu.find_element_by_xpath("//a[@data-feed-option-name=\"HIDE_FROM_TIMELINE\"]")
                    except SELENIUM_EXCEPTIONS:
                        delete_button = menu.find_element_by_xpath("//a[@data-feed-option-name=\"UNTAG\"]")

                actions.move_to_element(delete_button).click().perform()
                confirmation_button = driver.find_element_by_class_name("layerConfirm")

                click_button(driver, confirmation_button)

            except SELENIUM_EXCEPTIONS:
                continue
            else:
                break
        wall_log.close()

        # Required to sleep the thread for a bit after using JS to click this button
        time.sleep(5)
        driver.refresh()
