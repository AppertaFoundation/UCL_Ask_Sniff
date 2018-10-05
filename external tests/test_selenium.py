import django
import time
import re
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from iPoorly.models import Child, Category, Heading, AgeGroup, SubHeading, DiaryLog
from selenium import webdriver
from pyvirtualdisplay import Display


class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        self.vdisplay = Display(visible=0, size=(1024, 768))
        self.vdisplay.start()
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(SeleniumTest, self).setUp()

    def tearDown(self):
        # stop browser
        self.driver.quit()
        # stop display
        self.vdisplay.stop()
        super(SeleniumTest, self).tearDown()

    def test_selenium(self):

        def redirect(url):
            try:
                self.driver.get(url)
                pause()
            except:
                print("Error redirecting to homepage")

        def click_home():
            try:
                self.driver.find_element_by_link_text("Home").click()
                pause()
            except:
                print("Error clicking Home button in navbar")

        def click_select_age():
            try:
                self.driver.find_element_by_link_text("Select Age").click()
                pause()
            except:
                print("Error clicking Select Age button in navbar")

        def click_children():
            try:
                self.driver.find_element_by_link_text("Children").click()
                pause()
            except:
                print("Error clicking Children button in navbar")

        def click_diary():
            try:
                self.driver.find_element_by_link_text("Diary").click()
                pause()
            except:
                print("Error clicking Diary button in navbar")

        def click_logout():
            try:
                self.driver.find_element_by_link_text("Logout").click()
                pause()
            except:
                print("Error clicking Logout button in navbar")

        def click_map():
            try:
                self.driver.find_element_by_link_text("Map").click()
                pause()
            except:
                print("Error clicking Map button in navbar")

        def click_search():
            try:
                self.driver.find_element_by_link_text("Search").click()
                pause()
            except:
                print("Error clicking Search button in navbar")

        def click_999():
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/a/i").click()
                pause()
            except:
                print("Error clicking Calling 999 button in navbar")

        def click_close():  # For closing the 999 menu
            try:
                self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/a").click()
                # self.driver.find_element_by_id("close").click()
                pause()
            except:
                print("Error clicking close button. Most likely no close class found")

        def click_cancel():
            try:
                self.driver.find_element_by_xpath("/html/body/main/form/a").click()
                # self.driver.find_element_by_id("cancel").click()
                pause()
            except:
                print("Error clicking cancel button")

        def click_agree():
            try:
                self.driver.find_element_by_xpath("/html/body/main/form/button").click()
                # self.driver.find_element_by_id("agree").click()
                pause()
            except:
                print("Error clicking agree button.")

        def click_login_signup():
            try:
                self.driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/a").click()
                # self.driver.find_element_by_id("loginSignup").click()
                pause()
            except:
                print("Error clicking login/Signup button.")

        def click_skip_login():
            try:
                self.driver.find_element_by_xpath("/html/body/main/div[2]/div[2]/a").click()
                # self.driver.find_element_by_id("skipLogin").click()
                pause()
            except:
                print("Error clicking skip login button.")

        def click_submit():
            try:
                self.driver.find_element_by_xpath("/html/body/main/div/form/button").click()
                # self.driver.find_element_by_id("submit").click
                pause()
            except:
                print("Error clicking submit button.")

        def pause():
            try:
                time.sleep(0.5)
            except:
                print("Timer error in pause function")

        def check_url_is(url):
            pause()
            if (url == self.driver.current_url):
                return True
            return False

        def locate_text_in_page(text):  # checks source
            try:
                src = self.driver.page_source
                text_found = re.search(text, src)
                # print("Element found.")
                if (text_found):
                    print("Element found in source code")
                    return True
                else:
                    return False
                return True
            except:
                print("Element not found in source code")
                print("Element not found.")
                return False

        def go_to_form(newForm):  # can either be login or signup
            current_state = "none"
            try:
                self.driver.find_element_by_id("username").send_keys("test")
                self.driver.find_element_by_id("username").clear()
                pause()
            except:  # will go here if login button not found
                try:
                    self.driver.find_element_by_id("username2").send_keys("test")
                    self.driver.find_element_by_id("username2").clear()
                    pause()
                except:
                    print("Error finding username fields - form does not exist")
                    current_state = "none"
                else:
                    current_state = "signup"
            else:
                current_state = "login"

            if current_state == "none":
                print("Error switching forms. Form does not exist")
            elif current_state == "login" and newForm == "signup":
                self.driver.find_element_by_link_text("Sign Up").click()
                pause()
            elif current_state == "signup" and newForm == "login":
                self.driver.find_element_by_link_text("Login").click()
                pause()

        def enter_details(username, password):
            try:
                self.driver.find_element_by_id("username").send_keys(username)
                self.driver.find_element_by_id("password").send_keys(password)
                pause()
            except:
                try:
                    self.driver.find_element_by_id("username2").send_keys(username)
                    self.driver.find_element_by_id("password2").send_keys(password)
                    pause()
                except:
                    print("Error signing in username and password")

        def clear_details():
            try:
                self.driver.find_element_by_id("username").clear()
                self.driver.find_element_by_id("password").clear()
                pause()
            except:
                try:
                    self.driver.find_element_by_id("username2").clear()
                    self.driver.find_element_by_id("password2").clear()
                    pause()
                except:
                    print("Error clearing details - form does not exist")

        def submit_details():
            try:
                self.driver.find_element_by_id("login-button").click()
                pause()
            except:
                try:
                    self.driver.find_element_by_id("signup-button").click()
                    pause()
                except:
                    print("Error submitting details")

        def click_add_child():
            try:
                # self.driver.find_element_by_link_text("person add").click()
                self.driver.find_element_by_xpath("/html/body/main/a/i").click()
                pause()
            except:
                print("Error clicking add child button")

        def enter_child_details(name, dob):  # dob in form of yyyy-mm-dd
            try:
                self.driver.find_element_by_id("childName").send_keys(name)
                self.driver.find_element_by_id("dob").send_keys(dob)
                pause()
            except:
                print("Error entering child details")

        def clear_child_details():
            try:
                self.driver.find_element_by_id("childName").clear()
                self.driver.find_element_by_id("dob").clear()
                pause()
            except:
                print("Error clearing child details")

        def click_add_child_submit():
            try:
                # heres the problem > For every new child div increases by 1 so tricky to use xpath
                # self.driver.find_element_by_link_text("Add Child").click()
                self.driver.find_element_by_xpath("//button[contains(.,'Add Child')]").click()
                pause()
            except:
                print("Error clicking submit button to add child")

        def click_edit_child_submit():
            try:
                # heres the problem > For every new child div increases by 1 so tricky to use xpath
                # self.driver.find_element_by_link_text("Add Child").click()
                self.driver.find_element_by_xpath("//button[contains(.,'Edit Child')]").click()
                pause()
            except:
                print("Error clicking submit button to edit child")

        def click_click_here():
            try:
                self.driver.find_element_by_link_text("click here").click()
                pause()
            except:
                print("Error clicking 'click here' hyperlink")

        def click_delete_youngest_child():
            try:
                self.driver.find_element_by_xpath("/html/body/main/table/tbody/tr/td[3]/a[2]/i").click()
                pause()
            except:
                print("Error clicking delete button for youngest child")

        def click_edit_youngest_child():
            try:
                self.driver.find_element_by_xpath("/html/body/main/table/tbody/tr/td[3]/a[1]/i").click()
                pause()
            except:
                print("Error clicking delete button for youngest child")

        def accept_alert():
            try:
                self.driver.switch_to.alert.accept()
                pause()
            except:
                print("Error clicking Ok button for alert popup")

        def dismiss_alert():
            try:
                self.driver.switch_to_alert.dismiss()
                pause()
            except:
                print("Error dismissing alert popup")

        def click_text(tag_name, text):
            try:
                self.driver.find_element_by_xpath("//" + tag_name + "[contains(.,'" + text + "')]").click()
                pause()
            except:
                print("Error clicking text")

        def click_add_log():
            try:  # /html/body/main/a/i
                self.driver.find_element_by_xpath("/html/body/main/a/i").click()
                pause()
            except:
                print("Error clicking add diary log for child")

        def add_log_details(title, description):
            try:
                self.driver.find_element_by_id("id_title").send_keys(title)
                self.driver.find_element_by_id("id_text").send_keys(description)
                pause()
            except:
                print("Error adding log details")

        def submit_log_details():
            try:
                self.driver.find_element_by_xpath("//button[contains(.,'Add Log')]").click()
                pause()
            except:
                try:
                    self.driver.find_element_by_xpath("//button[contains(.,'Edit Log')]").click()
                    pause()
                except:
                    print("Error submitting log details")

        def clear_log_details():
            try:
                self.driver.find_element_by_id("id_title").clear()
                self.driver.find_element_by_id("id_text").clear()
                pause()
            except:
                print("Error clearing log details")

        def delete_first_log_entry():
            try:
                self.driver.find_element_by_xpath("/html/body/main/div[1]/p[3]/a[2]/i").click()
                pause()
            except:
                print("Error deleting latest log entry")

        def edit_first_log_entry():
            try:
                self.driver.find_element_by_xpath("/html/body/main/div[1]/p[3]/a[1]/i").click()
                pause()
            except:
                print("Error editing latest log entry")

        # This is where the main function sort of starts
        # Need to store the URLs of the pages...
        home_url = "http://localhost:8000/"
        disclaimer_url = home_url + "disclaimer/"
        homepage_url = home_url + "homepage/"
        no_user_my_child_url = home_url + "noUser/age/"
        no_user_map_url = home_url + "map/"
        no_user_search_url = home_url + "search/"
        signup_url = home_url + "accounts/signup/"
        my_child_url = home_url + "myChild/"
        edit_child_url = home_url + "child/manage/"
        diary_url = home_url + "diary/"

        print(" ")
        print("---Login + Signup Test---")

        redirect(home_url)

        redirect(home_url)
        print("No username signup test...")
        try:
            click_login_signup()
            go_to_form("signup")
            enter_details("", "jalapeno")
            submit_details()
        except:
            print("Error entering incorrect details.	X")
        else:
            if check_url_is(home_url):
                print("No username signup test passed")
            else:
                print("No username signup test failed	X")

        redirect(home_url)
        print("No password signup test...")
        try:
            click_login_signup()
            go_to_form("signup")
            enter_details("spicy", "")
            submit_details()
        except:
            print("Error entering incorrect details.	X")
        else:
            if check_url_is(home_url):
                print("No password signup test passed")
            else:
                print("No password signup test failed	X")

        redirect(home_url)
        print("Existing username signup test...")
        try:
            click_login_signup()
            go_to_form("signup")
            enter_details("admin", "jalapeno")
            submit_details()
        except:
            print("Error entering incorrect details.	X")
        else:
            if check_url_is(signup_url):
                print("Existing username signup test passed")
            else:
                print("Existing username signup test failed	X")

        redirect(home_url)
        print("No username login test...")
        try:
            click_login_signup()
            enter_details("", "jalapeno")
            submit_details()
        except:
            print("Error entering incorrect details.	X")
        else:
            if check_url_is(home_url):
                print("No username login test passed")
            else:
                print("No username login test failed	X")

        redirect(home_url)
        print("No password login test...")
        try:
            click_login_signup()
            enter_details("spicy", "")
            submit_details()
        except:
            print("Error entering incorrect details.	X")
        else:
            if check_url_is(home_url):
                print("No password login test passed")
            else:
                print("No password login test failed	X")

        redirect(home_url)
        print("Working user login test...")
        try:
            click_login_signup()
            enter_details("zo", "zo")
            submit_details()
            # should be on disclaimer page at this point
            click_agree()
        except:
            print("Error entering working login test	X.")
        else:
            if check_url_is(homepage_url) or check_url_is(my_child_url):
                print("Working login test passed")
            else:
                print("Working login test failed	X")

        click_close()
        print("Logout test...")
        try:
            click_logout()
        except:
            print("Error logging out	X.")
        else:
            if check_url_is(home_url):
                print("Logout test passed")
            else:
                print("Logout test failed	X")

        print(" ")
        print("---Normal User Testing---")

        redirect(home_url)
        print("Logging in as normal user...")
        try:
            click_login_signup()
            enter_details("zo", "zo")
            submit_details()
            # should be on disclaimer page at this point
            click_agree()
        except:
            print("Error logging in as user	X")
        else:
            if check_url_is(homepage_url) or check_url_is(my_child_url):
                print("Logged in succesfully")
            else:
                print("Not logged in as zo	X")

        redirect(my_child_url)
        print("Over-aged child testing...")
        try:
            click_add_child()
            enter_child_details("zozob", "2008-11-11")
            click_add_child_submit()
        except:
            print("Error adding overaged child	X")
        else:
            if not locate_text_in_page("zozob"):
                print("Adding over-aged child test passed")
            else:
                print("Adding over-aged child test failed	X")

        redirect(my_child_url)
        print("Adding child testing...")
        try:
            click_add_child()
            enter_child_details("Test Jr", "2017-11-11")
            click_add_child_submit()
        except:
            print("Error adding child into database	X")
        else:
            if locate_text_in_page("Test Jr"):
                print("Adding child test passed")
            else:
                print("Adding child test failed	X")

        redirect(edit_child_url)
        print("Editing child testing...")
        try:
            click_edit_youngest_child()
            clear_child_details()
            enter_child_details("Test Junior", "2017-11-11")
            click_edit_child_submit()
            redirect(my_child_url)
        except:
            print("Error editing youngest child")
        else:
            if locate_text_in_page("Test Junior"):
                print("Editing child test passed")
            else:
                print("Editing child test failed	X")

        redirect(edit_child_url)
        print("Deleting child testing...")
        try:
            click_delete_youngest_child()
            accept_alert()
            redirect(my_child_url)
        except:
            print("Error deleting youngest child	X")
        else:
            if not locate_text_in_page("Test Junior"):
                print("Deleting child test passed")
            else:
                print("Deleting child test failed	X")

        redirect(diary_url)
        print("Go to child diary log testing...")
        try:
            click_text("a", "zozoa")
        except:
            print("Error going to selected child's diary log	X")
        else:
            # Diary entries of child
            if locate_text_in_page("Diary entries of Zozoa"):
                print("Going to child's diary log test passed")
            else:
                print("Going to child's diary log test failed	X")

        print("Adding diary log entry testing...")
        try:
            click_add_log()
            add_log_details("test-title", "lots of spots")
            submit_log_details()
        except:
            print("Error adding diary log entry	X")
        else:
            if locate_text_in_page("test-title") and locate_text_in_page("lots of spots"):
                print("Adding diary log entry test passed")
            else:
                print("Adding diary log entry test failed	X")

        print("Delete diary log entry testing...")
        try:
            delete_first_log_entry()
            accept_alert()
            redirect(diary_url)
            click_text("a", "zozoa")
        except:
            print("Error deleting diary log entry	X")
        else:
            if not locate_text_in_page("test-title"):
                print("Delete diary log entry test passed")
            else:
                print("Delete diary log entry test failed	X")

        redirect(homepage_url)
        click_close()
        click_logout()

        print(" ")
        print("---Userless Navigation Testing---")

        redirect(home_url)
        print("Skipping login test...")
        try:
            click_skip_login()
        except:
            print("Error skipping login test	X")
        else:
            if check_url_is(disclaimer_url):
                print("Skipping login test passed")
            else:
                print("Skipping login test failed	X")

        redirect(disclaimer_url)
        print("Cancelling disclaimer test...")
        try:
            click_cancel()
        except:
            print("Error cancelling disclaimer test	X")
        else:
            if check_url_is(home_url):
                print("Cancelling disclaimer test passed")
            else:
                print("Cancelling disclaimer test failed	X")

        redirect(home_url)
        click_skip_login()
        print("Agreeing disclaimer test...")

        try:
            click_agree()
        except:
            print("Error agreeing disclaimer  test	X")
        else:
            if check_url_is(no_user_my_child_url):
                print("Agreeing disclaimer test passed")
            else:
                print("Agreeing disclaimer test failed	X")

        redirect(homepage_url)
        print("Submit button for age selection test...")
        try:
            click_submit()
        except:
            print("Error clicking submit button for age selection test	X")
        else:
            if check_url_is(homepage_url):
                print("Submit button for age selection test passed")
            else:
                print("Submit button for age selection test failed	X")

        redirect(homepage_url)
        click_close()
        print("Clicking home navbutton test...")
        try:
            click_home()
        except:
            print("Error clicking home navbutton test	X")
        else:
            if check_url_is(homepage_url):
                print("Clicking home navbutton test passed")
            else:
                print("Clicking home navbutton test failed	X")

        redirect(homepage_url)
        click_close()
        print("Clicking select age navbutton test...")
        try:
            click_select_age()
        except:
            print("Error clicking select age navbutton test	X")
        else:
            if check_url_is(no_user_my_child_url):
                print("Clicking select age navbutton test passed")
            else:
                print("Clicking select age navbutton test failed	X")

        redirect(homepage_url)
        click_close()
        print("Clicking map navbutton test...")
        try:
            click_map()
        except:
            print("Error clicking map navbutton test	X")
        else:
            if check_url_is(no_user_map_url):
                print("Clicking map navbutton test passed")
            else:
                print("Clicking map navbutton test failed	X")

        redirect(homepage_url)
        click_close()
        print("Clicking search navbutton test...")
        try:
            click_search()
        except:
            print("Error clicking search navbutton test	X")
        else:
            if check_url_is(no_user_search_url):
                print("Clicking search navbutton test passed")
            else:
                print("Clicking search navbutton test failed	X")

        redirect(homepage_url)
        click_close()
        print("Clicking 999 navbutton test...")
        try:
            click_999()
        except:
            print("Error clicking 999 navbutton test	X")
        else:
            if locate_text_in_page("modal modal-fixed-footer open"):  # class name in page src
                print("Clicking 999 navbutton test passed")
                print("Closing 999 popup test...")
                try:
                    click_close()
                except:
                    print("Error closing 999 popup	X")
                else:
                    if locate_text_in_page("modal modal-fixed-footer"):
                        print("Close 999 popup test passed")
                    else:
                        print("Close 999 popup test failed	X")
            else:
                print("Clicking 999 navbutton test failed	X")
                print("Cannot attempt close navbar testing. Skipping	X")
