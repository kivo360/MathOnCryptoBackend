"""OS Modules environ method to get the setup vars from the Environment"""
from datetime import datetime
from os import environ
from random import randint
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from .open_page import open_coin_page
from .table_search import get_webpage_text

class CoinMiner:
  """Class to be instantiated to use the script"""
  def __init__(self, nogui=False):
    if nogui:
      self.display = Display(visible=0, size=(800, 600))
      self.display.start()

    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
    self.browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)
    self.browser.implicitly_wait(25)

    self.logFile = open('./logs/logFile.txt', 'a')
    self.logFile.write('Session started - %s\n' \
                       % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    self.nogui = nogui


  def open_webpage(self):
    open_coin_page(self.browser)
    return self
  
  def get_website_text(self):
    print get_webpage_text(self.browser)
    return self

  def end(self):
    """Closes the current session"""
    self.browser.delete_all_cookies()
    self.browser.close()

    if self.nogui:
      self.display.stop()

    print('')
    print('Session ended')
    print('-------------')

    self.logFile.write(
      '\nSession ended - {}\n'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      )
    )
    self.logFile.write('-' * 20 + '\n\n')
    self.logFile.close()

