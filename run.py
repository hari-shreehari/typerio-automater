import time
import pytesseract
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import io
import pyautogui
import random

# Set up the Firefox WebDriver
service = Service()  # Default path will be used
driver = webdriver.Firefox(service=service)

# Open the URL
driver.get('https://typer.io/solo')
time.sleep(5)  # Wait for the page to load fully

# Maximize the window
driver.maximize_window()

# Define the area for taking the screenshot (coordinates and dimensions)
left = 630
top = 350
width = 650
height = 440

# Take a full screenshot
screenshot = driver.get_screenshot_as_png()

# Convert the screenshot to a PIL Image
image = Image.open(io.BytesIO(screenshot))

# Define the area to capture from the full screenshot
area = (left, top, left + width, top + height)

# Extract the specific area from the image
screenshot_area = image.crop(area)

# Use Tesseract to extract text from the screenshot
extracted_text = pytesseract.image_to_string(screenshot_area)
extracted_text = ' '.join(extracted_text.split())
final_text = []

for i in extracted_text:
    if not i.isalpha() and not final_text:
        pass
    elif i == "|":
        final_text.append('I')
    else:
        final_text.append(i)

typed_text = ''.join(final_text)
print(typed_text)  # Print the extracted text to console

# Locate the parent div and click on it
input_container = driver.find_element(By.CSS_SELECTOR, "div.Editor_container__DN_YS")
ActionChains(driver).move_to_element(input_container).click().perform()

# Wait for a moment to ensure the input field is focused
time.sleep(1)

pyautogui.typewrite(' ')
# Wait for 4 seconds before typing
time.sleep(5)
# Type the extracted text with random delays
for char in typed_text:
    pyautogui.typewrite(char)
    random_delay = random.uniform(0.0002, 0.02)      
    time.sleep(random_delay)

# Close the driver
driver.quit()

