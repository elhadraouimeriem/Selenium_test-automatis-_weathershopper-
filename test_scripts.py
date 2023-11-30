from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# logging.basicConfig(level=logging.INFO)
x = datetime.datetime.now()

def test_google_search():
    # Instantiate the driver object
    driver = webdriver.Edge()
    driver.maximize_window()

    # Navigate to weathershopper.pythonanywhere.com
    driver.get("https://weathershopper.pythonanywhere.com/")

    # Verify the URL of the page
    assert driver.current_url == "https://weathershopper.pythonanywhere.com/", "Ce n'est pas la bonne URL"

    # Take a screenshot of the page
    driver.save_screenshot(f'screenshots/screenshot-{x.year}-{x.month}-{x.day}_{x.hour}_{x.minute}_{x.second}.png')

    # Update the assertion for the title
    assert driver.title == "Current Temperature", "Mauvais titre de la page"

    moisture_button_xpath = "/html/body/div/div[3]/div[1]/a/button"
    sunscreen_button_xpath = "/html/body/div/div[3]/div[2]/a/button"

    # Extract the temperature value and convert it to an integer
    temperature_text = driver.find_element(By.ID, "temperature").text
    temperature = int(temperature_text.split()[0])  # Extract the numeric part

    # Shop for moisturizers if the weather is below 19 degrees
    if temperature < 19:
        product_names = ['Almond', 'Aloe']
        moisture_button = driver.find_element(By.XPATH, moisture_button_xpath)
        moisture_button.click()
        print("Shopping for moisturizers.")

    # Shop for sunscreens if the weather is above 34 degrees
    elif temperature > 34:
        product_names = ['SPF-50', 'SPF-30']
        sunscreen_button = driver.find_element(By.XPATH, sunscreen_button_xpath)
        sunscreen_button.click()
        print("Shopping for sunscreens.")
        
    # Add an else statement if you want to handle temperatures between 19 and 34
    else:
        print("The weather is between 19 and 34 degrees. No shopping needed.")

    selected_products = []  # List to store selected products

    for product_name in product_names:
        # Convert the product name to lowercase for case-insensitive comparison
        product_name_lower = product_name.lower()

        # Locate all products containing the current product name
        product_elements = driver.find_elements(By.XPATH, f'//p[contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{product_name_lower}")]')

        # Iterate through each product and find the minimum-priced one
        min_price = float('inf')
        min_price_product = None

        for product_element in product_elements:
            # Extract the price
            price_element = product_element.find_element(By.XPATH, './/following-sibling::p')
            price_text = price_element.text.replace("Price: Rs. ", "")
            price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))

            if price < min_price:
                min_price = price
                min_price_product = product_element

        # Click on the "Add" button for the minimum-priced product
        if min_price_product is not None:
            add_button = min_price_product.find_element(By.XPATH, './/following-sibling::button[text()="Add"]')
            add_button.click()
            selected_products.append(product_name)  # Add the selected product to the list

    # Click on the cart and proceed with the payment for all selected products
    if selected_products:
        
        cart = driver.find_element(By.XPATH, "/html/body/nav/ul/button")
        cart.click()

        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/button").click()

        # Switch to the iframe for payment
        driver.switch_to.frame(0)
        formulaire = [
            driver.find_element(By.ID, "email"),
            driver.find_element(By.ID, "card_number"),
            driver.find_element(By.ID, "cc-exp"),
            driver.find_element(By.ID, "cc-csc")
        ]

        creditcard = ["m.elhadraoui@mundiapolis.ma", "4242424242424242", "1224", "333"]

        def typeslowly(loc, text):
            for i in text:
                loc.send_keys(i)

        for i in range(4):
            typeslowly(formulaire[i], creditcard[i])

        # Wait for the element with ID "billing-zip" to be present
        zip_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'billing-zip'))
        )

        # Once the element is present, send keys
        zip_element.send_keys("24")

        # Wait for the element with ID "submitButton" to be present
        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="submitButton"]'))
        )

        # Once the button is present, click on it
        submit_button.click()

        # Switch back to the main frame
        driver.switch_to.default_content()

    time.sleep(5)
    driver.quit()

# Call the function
if __name__ == "__main__":
    test_google_search()
