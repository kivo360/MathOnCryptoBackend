from .time_util import sleep
from selenium.webdriver.common.action_chains import ActionChains
try:
    import cPickle as pickle
except:
    import pickle


def get_webpage_text(browser):
    """
    //table[@id="currencies"]/tbody/tr/td[1]
    """
    links = get_list_of_links(browser)
    sleep(3)
    out_s = open('all_text_data.pickle', 'wb')
    try:
        for link in links:
            name = checkout_page(browser, link)
            text_data = mine_page_text(browser)
            pickle.dump({name: text_data}, out_s)
    finally:
        out_s.close()
    
        


def get_list_of_links(browser):
    rows = browser.find_elements_by_xpath('//table[@id="currencies"]/tbody/tr/td[2]')
    list_of_links = []
    for row in rows:
        list_of_links.append(row.find_element_by_tag_name('a').get_attribute('href'))
    return list_of_links
def checkout_page(browser, link):
    browser.get(link)
    # .bottom-margin-2x > div.col-xs-4.col-sm-4 > ul
    element_container = browser.find_element_by_css_selector('.bottom-margin-2x > div.col-xs-4.col-sm-4 > ul')
    crypto_website_link = element_container.find_elements_by_tag_name('a')[0].get_attribute('href')
    name_text = browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[3]/div[1]/h1').text
    browser.get(crypto_website_link)
    
    return name_text

def mine_page_text(browser):
    sleep(8)
    all_tags = []
    tag_text = []
    all_p_tags = browser.find_elements_by_tag_name('p')
    for i in all_p_tags:
        tag_text.append(i.text)
    
    print "checkpoint"
    all_h1_tags = browser.find_elements_by_tag_name('h1')
    for i in all_h1_tags:
        tag_text.append(i.text)
    print "checkpoint"
    all_h2_tags = browser.find_elements_by_tag_name('h2')
    for i in all_h2_tags:
        tag_text.append(i.text)
    print "checkpoint"
    print tag_text
    return tag_text
    
    
def get_tags_text(tags_list):
    tags_text = []
    for tag in tags_list:
        print tag
        tags_list.append(tag.text)
    return tags_text