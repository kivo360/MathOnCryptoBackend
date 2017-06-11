from coinminer import CoinMiner



# If you want to enter your Instagram Credentials directly just enter
# username=<your-username-here> and password=<your-password> into InstaPy
# e.g like so InstaPy(username="instagram", password="test1234")

CoinMiner(nogui=True)\
  .open_webpage()\
  .get_website_text()\
  .end()
