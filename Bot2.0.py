from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, json

class instagramBot():
    def __init__(self, file_name, base_page):
        with open(file_name, encoding="utf-8") as file:
            raw_file = file.read()
            login = json.loads(raw_file)
        self.username = login["username"]
        self.password = login["password"]
        self.driver = webdriver.Chrome()
        self.basePage = base_page
        self.accountsRegister =  open("accounts.db", "a", encoding="utf-8")

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/?hl=en")
        usernameElement = driver.find_elements_by_name("username")[0]
        usernameElement.clear()
        usernameElement.send_keys(self.username)
        time.sleep(0.5)
        passwordElement = driver.find_elements_by_name("password")[0]
        passwordElement.clear()
        passwordElement.send_keys(self.password)
        time.sleep(0.5)
        passwordElement.submit()
        time.sleep(4)
        ignoreNotificationsElement = driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0]
        ignoreNotificationsElement.click()
        time.sleep(0.5)

    def getAccountsNames(self, number_of_accounts_to_follow):
        driver = self.driver
        basePage = self.basePage
        accountsRegister = self.accountsRegister
        ## Getting the account names ##
        driver.get("https://www.instagram.com/" + basePage + "/?hl=en")
        time.sleep(0.5)
        followersButton = driver.find_elements_by_xpath("//a[contains(@class, '-nal3')]")[0]
        followersButton.click()
        time.sleep(1)
        account_counter = 0
        driver.execute_script('document.querySelector(".isgrP").scrollBy(0,400)')
        time.sleep(0.5)
        driver.execute_script('document.querySelector(".isgrP").scrollBy(0,-400)')
        time.sleep(0.5)
        baseFollowers = driver.find_elements_by_xpath("//li[contains(@class, 'wo9IH')]")
        while account_counter < number_of_accounts_to_follow:
            for profile in baseFollowers:
                profileName = profile.find_elements_by_class_name("FPmhX")[0].text
                account_counter += 1
                driver.execute_script('document.querySelector(".isgrP").scrollBy(0,54)')
                time.sleep(0.05)
                print(profileName)#############
                accountsRegister.write(profileName + "\n")
            baseFollowers = driver.find_elements_by_xpath("//li[contains(@class, 'wo9IH')]")[account_counter:]

    def follow(self, delay):
        ## Getting the acounts to follow ##
        driver = self.driver
        accountsRegister = self.accountsRegister
        accounts_file_raw = open("accounts.db", "r").readlines()
        accounts_to_follow = []
        for account in accounts_file_raw:
            accounts_to_follow.append(account.replace("\n", ""))
        ## Going to page and following ##
        following_accounts = open("following.db", "a")
        for account in accounts_to_follow:
            driver.get("https://www.instagram.com/" + account + "/?hl=en")
            time.sleep(1)
            follow_button = driver.find_elements_by_xpath("//button")
            following_status = follow_button[0].text if follow_button[0].text == "Follow" else follow_button[1].text
            if following_status == "Follow":
                try:
                    if follow_button[1].text == "Follow":
                        follow_button[1].click()
                    else:
                        follow_button[0].click()
                    following_accounts.write(account + "\n")
                except:
                    pass
            time.sleep(delay)
        following_accounts.close()
    def unfollow(self,delay):
        ## Getting the acounts to follow ##
        driver = self.driver
        raw_following_accounts = open("following.db", "r")
        following_accounts = []
        for account in raw_following_accounts:
            following_accounts.append(account.replace("\n", ""))
        following_requested_button = driver.find_elements_by_xpath("//button")
        for account in following_accounts:
            driver.get("https://www.instagram.com/" + account + "/?hl=en")
            if following_requested_button[1].text == "Following" or following_requested_button[1] == "Requested":
                following_requested_button[1].click()
            else:
                following_requested_button[0].click()
            time.sleep(delay)
        raw_following_accounts.close()
        open("following.db", "w").write("")

    def close(self):
        self.driver.close()
        self.accountsRegister.close()

bot = instagramBot("login.json", "mendigods")
bot.login()

#bot.getAccountsNames(1000)

bot.follow(1)
bot.unfollow(1)

## bot.close()