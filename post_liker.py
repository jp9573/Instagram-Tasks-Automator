import utils
import time


def url_name(url):
    # the web page opens up
    chrome_driver.get(url)

    # webdriver will wait for 4 sec before throwing a
    # NoSuchElement exception so that the element
    # is detected and not skipped.
    time.sleep(4)


def first_picture():
    # finds the first picture
    pic = chrome_driver.find_element_by_class_name("_9AhH0")
    pic.click()  # clicks on the first picture


def like_pic():
    time.sleep(4)
    like = chrome_driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span')

    time.sleep(2)
    like.click()  # clicking the like button


def next_picture():
    time.sleep(2)

    # finds the button which gives the next picture
    # nex = chrome.find_element_by_class_name("HBoOv")
    nex = chrome_driver.find_element_by_xpath("//a[contains(.,'Next')]")

    time.sleep(1)
    return nex


def continue_liking():
    while (True):
        next_el = next_picture()

        # if next button is there then
        if next_el != False:

            # click the next button
            next_el.click()
            time.sleep(2)

            # like the picture
            like_pic()
            time.sleep(2)
        else:
            print("not found")
            break


chrome_driver = utils.get_driver()
time.sleep(1)

url_name(utils.URL)

utils.login(chrome_driver, utils.USERNAME, utils.PASSWORD)
first_picture()
like_pic()

continue_liking()
