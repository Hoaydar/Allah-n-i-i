import undetected_chromedriver as webdriver
 
# Create an instance of the undetected ChromeDriver in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
 
# Navigate to target website
driver.get("https://www.g2.com/products/asana/reviews")
 
# Take a screenshot
driver.save_screenshot("screenshot.png")
 
# Close the browser
driver.quit()
