from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time

# --------------------------------------------------
# Browser configuration and startup
# --------------------------------------------------
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)

# Open Cookie Clicker in browser
browser.get("https://ozh.github.io/cookieclicker/")

# Give the page time to fully initialise
sleep(3)

# --------------------------------------------------
# Language selection (English)
# --------------------------------------------------
print("Checking for language menu...")
try:
    english_button = browser.find_element(By.ID, "langSelect-EN")
    english_button.click()
    print("English selected")
    sleep(3)
except NoSuchElementException:
    print("Language menu already set or not found")

# Extra pause to ensure UI loads correctly
sleep(2)

# --------------------------------------------------
# Core game elements
# --------------------------------------------------
big_cookie = browser.find_element(By.ID, "bigCookie")

# Timer controls
purchase_interval = 5
next_purchase_check = time() + purchase_interval
end_time = time() + 300  # 5 minutes total runtime

# --------------------------------------------------
# Main automation loop
# --------------------------------------------------
while True:
    # Click the cookie continuously
    big_cookie.click()

    # Periodically attempt to buy upgrades
    if time() >= next_purchase_check:
        try:
            # Read current cookie total
            cookie_display = browser.find_element(By.ID, "cookies").text
            current_cookies = int(cookie_display.split()[0].replace(",", ""))

            # Fetch all store items
            store_items = browser.find_elements(By.CSS_SELECTOR, "div[id^='product']")

            # Choose the most expensive affordable upgrade
            affordable_item = None
            for item in reversed(store_items):
                if "enabled" in item.get_attribute("class"):
                    affordable_item = item
                    break

            if affordable_item:
                affordable_item.click()
                print(f"Purchased: {affordable_item.get_attribute('id')}")

        except (NoSuchElementException, ValueError):
            print("Error reading cookies or store items")

        # Schedule next upgrade attempt
        next_purchase_check = time() + purchase_interval

    # End script after time limit
    if time() >= end_time:
        try:
            final_score = browser.find_element(By.ID, "cookies").text
            print(f"Automation complete — {final_score}")
        except NoSuchElementException:
            print("Unable to retrieve final score")
        break
