from selenium import webdriver # This line imports the webdriver module from the selenium package. The webdriver module provides a way to interact with web browsers and automate browser actions.
from selenium.webdriver.common.by import By # This line imports the By class from the selenium.webdriver.common package. The By class defines locator strategies for finding elements within a web page, such as by ID, name, class name, tag name, CSS selector, or XPath.
from selenium.webdriver.support.ui import WebDriverWait # This line imports the WebDriverWait class from the selenium.webdriver.support.ui package. The WebDriverWait class provides a way to wait for a certain condition to occur before proceeding with code execution, such as waiting for an element to become visible or clickable.
from selenium.webdriver.support import expected_conditions as EC # This line imports the expected_conditions module from the selenium.webdriver.support package and aliases it as EC. The expected_conditions module contains a set of predefined conditions that can be used with WebDriverWait to wait for specific events or states.

# Config
screenshotDir = "Screenshots" # This line sets the screenshotDir variable to the string "Screenshots". This variable presumably defines the directory where screenshots will be saved.
screenWidth = 400 # This line sets the screenWidth variable to the integer 400. This variable likely defines the width of the browser window or the width of the screenshot to be captured.
screenHeight = 800 # This line sets the screenHeight variable to the integer 800. This variable likely defines the height of the browser window or the height of the screenshot to be captured.

def getPostScreenshots(filePrefix, script): # This line defines the getPostScreenshots function, which takes two parameters: filePrefix (a string used as a prefix for the screenshot filenames) and script (an instance of the VideoScript class).
    print("Taking screenshots...") # This line prints a message indicating that the function is taking screenshots.
    driver, wait = __setupDriver(script.url) # This line calls the private function __setupDriver with the script.url as its argument. The function likely initializes the Selenium WebDriver and navigates to the specified URL. The function returns two objects: driver (the WebDriver instance) and wait (a WebDriverWait instance used for waiting for specific conditions).
    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait) # This line calls the private function __takeScreenshot with the arguments filePrefix, driver, and wait. The function presumably takes a screenshot of the browser window and saves it with a filename prefixed by filePrefix. The resulting filename is assigned to the titleSCFile attribute of the script object.
    for commentFrame in script.frames: # This line starts a loop that iterates over each commentFrame in the script.frames list.
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"t1_{commentFrame.commentId}") #  Inside the loop, this line calls the private function __takeScreenshot with the arguments filePrefix, driver, wait, and a formatted string containing the comment ID. The function likely takes a screenshot of the comment and saves it with a filename prefixed by filePrefix. The resulting filename is assigned to the screenShotFile attribute of the commentFrame object.
    driver.quit() # After the loop, this line closes the browser window and terminates the WebDriver session, releasing its resources.

def __takeScreenshot(filePrefix, driver, wait, handle="Post"): # This line defines the private function __takeScreenshot, which takes four parameters: filePrefix (a string used as a prefix for the screenshot filenames), driver (a WebDriver instance), wait (a WebDriverWait instance), and handle (a string representing the target element, with a default value of "Post").
    method = By.CLASS_NAME if (handle == "Post") else By.ID # This line sets the method variable based on the value of handle. If the handle is "Post", the method is set to By.CLASS_NAME. Otherwise, the method is set to By.ID. This variable will be used to locate the target element on the web page.
    search = wait.until(EC.presence_of_element_located((method, handle))) # This line uses the WebDriverWait wait object to wait for the target element to be present on the page. The presence_of_element_located function from the expected_conditions module (aliased as EC) is used to define the condition. The search variable is assigned the reference to the located element.
    driver.execute_script("window.focus();") # This line executes a JavaScript snippet in the browser window using the WebDriver instance driver. The script focuses the browser window, ensuring that the target element is visible for the screenshot.

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png" # This line creates a formatted string containing the screenshot filename, which includes the screenshotDir, filePrefix, and handle. The string is assigned to the fileName variable.
    fp = open(fileName, "wb") # This line opens a new file with the specified fileName in binary write mode and assigns the file object to the fp variable.
    fp.write(search.screenshot_as_png) # This line writes the screenshot of the target element (search) in PNG format to the file object fp.
    fp.close() # This line closes the file object fp, ensuring that the screenshot data is properly saved to the file.
    return fileName # This line returns the fileName variable, which contains the full path of the saved screenshot file.

'''
In summary, the __takeScreenshot function captures a screenshot of a specific element on a web page using Selenium WebDriver. The function locates the target element based on its handle, focuses the browser window, and saves a screenshot of the element with a specified filename prefix. The function then returns the full path of the saved screenshot file.
'''

def __setupDriver(url: str): # This line defines the private function __setupDriver, which takes one parameter: url (a string representing the target web page URL).
    options = webdriver.FirefoxOptions() # This line initializes a new FirefoxOptions object from the webdriver module and assigns it to the variable options. The FirefoxOptions object is used to configure the behavior of the Firefox WebDriver instance.
    options.headless = False # This line sets the headless attribute of the options object to False. When set to True, the Firefox WebDriver would run in headless mode, meaning it would not display a user interface. By setting it to False, the WebDriver will display the browser window.
    options.enable_mobile = False # This line sets the enable_mobile attribute of the options object to False. This attribute is not a standard Firefox option. It may be an attempt to disable mobile emulation, but the correct attribute to use would be options.set_preference("devtools.responsiveUI.customWidth", screenWidth) and options.set_preference("devtools.responsiveUI.customHeight", screenHeight).
    driver = webdriver.Firefox(options=options) # This line initializes a new Firefox WebDriver instance using the configured options object and assigns it to the variable driver.
    wait = WebDriverWait(driver, 10) # This line initializes a new WebDriverWait instance using the driver object and a timeout value of 10 seconds. The wait object will be used for waiting for specific conditions on the web page.

    driver.set_window_size(width=screenWidth, height=screenHeight) # This line sets the size of the browser window using the global variables screenWidth and screenHeight.
    driver.get(url) #  This line navigates the WebDriver to the specified url.

    return driver, wait # This line returns the driver (the initialized WebDriver instance) and wait (the WebDriverWait instance) objects.

'''
In summary, the __setupDriver function initializes a Selenium WebDriver instance with specific options, sets the window size, navigates to the provided URL, and returns the WebDriver and WebDriverWait instances for further interaction with the web page.
'''