from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class InstagramBot():
    def __init__(self, email, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        #path to chromerdriver.exe
        self.browser = webdriver.Chrome(executable_path ="C:\Program Files (x86)\Google\Chrome\chromedriver.exe", chrome_options=self.browserProfile) 
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')

        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        ui.WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()

    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text != 'Following'):
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")
    
    def unfollowWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Following'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")

    def likerecentpost(self):
        self.browser.get('https://www.instagram.com')
        rp = self.browser.find_element_by_class_name('dCJp8')
        span = rp.find_element_by_css_selector('span').get_attribute('aria-label')
        
        if(span == 'Like'):
            rp.click()
        time.sleep(2)
        self.browser.refresh()
        
    
    def getUserFollowers(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        bod = self.browser.find_element_by_css_selector('body').get_attribute('class')
        if bod == ' p-error dialog-404':
            print("Invalid Username.")
        else:
            followButton = self.browser.find_element_by_css_selector('button')
            temp = self.browser.find_element_by_css_selector('a').get_attribute('class')
            if (followButton.text == 'Following') or (temp == ' JNjtf'):
                followersLink = self.browser.find_element_by_css_selector('ul li a')
                followersLink.click()
                time.sleep(2)
                followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
                numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            
                followersList.click()
                actionChain = webdriver.ActionChains(self.browser)
                while (numberOfFollowersInList < max):
                    actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                    numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
                    print(numberOfFollowersInList)
                
                followers = []
                for user in followersList.find_elements_by_css_selector('li'):
                    userLink = user.find_element_by_css_selector('a').get_attribute('href')
                    print(userLink)
                    followers.append(userLink)
                    if (len(followers) == max):
                        break
                return followers
            else:
                print("You are not following this user")


    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


print("\n\n")
print("Instagram Bot".center(50,' '))
uname = input("Enter Unsername : ")
pwd = input("Enter Password : ")
bot = InstagramBot(uname, pwd)
bot.signIn()
while True:
    print("\n1.LIKE Recent Post\n2.Follow a User\n3.Unfollow a User\n4.Get a User's Followers\n5.Exit")
    choose = int(input(">>> "))
    choice = choose
    if choice == 5:
        bot.closeBrowser()
        break
    elif choice == 1:
        bot.likerecentpost()
    elif choice == 2:
        user = input("Enter Username to Follow : ")
        bot.followWithUsername(user)
    elif choice == 3:
        user = input("Enter Username to UnFollow : ")
        bot.unfollowWithUsername(user)
    elif choice == 4:
        user = input("Enter Username to get Followers : ")
        bot.getUserFollowers(user,100)
    else:
        print("Invalid choice, please choose again\n")
