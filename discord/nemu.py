from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from better_profanity import profanity
from selenium import webdriver
from datetime import datetime
import asyncio
import base64
import time
import re
import os

class WaifuGenerator:
    def __init__(self, prompts: str, website:str = 'https://waifus.nemusona.com/') -> None:
        self.driver = None
        self.original_prompts = prompts
        self.prompts = self.__filter_nsfw_prompts(prompts)
        self.prompts = self.__parse_prompts(self.prompts)
        self.service_path = '/usr/local/bin/geckodriver'
        self.website = website

    def __start_browser(self) -> None:
        service = Service(executable_path=self.service_path)
        self.driver = webdriver.Firefox(service=service)

    def __stop_browser(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None

    def __wait_for_page_to_load(self, timeout: int = 30) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState === 'complete';")
            )
            return True
        except TimeoutException:
            return False

    def __wait_for_image_change(self, timeout=900):
        old_src = self.driver.find_element(By.XPATH, "//img[@alt='image']").get_attribute('src')
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(By.XPATH, "//img[@alt='image']").get_attribute('src') != old_src
        )
    
    def __filter_nsfw_prompts(self, prompts):
        # Split prompts by comma, remove any NSFW prompts
        prompt_list = prompts.split(',')
        filtered_prompts = [p.strip() for p in prompt_list if not profanity.contains_profanity(p)]
        
        # Join the remaining prompts back into a string
        cleaned_prompts = ', '.join(filtered_prompts)
        return cleaned_prompts

    def __parse_prompts(self, prompts: str) -> str:
        prompt_list = prompts.split(',')
        cleaned_prompts = [p.strip().replace(' ', '_') for p in prompt_list]
        return ' '.join(cleaned_prompts)
    
    def __parse_filename(self) -> str:
        website_name = re.sub(r'^https?://|\.com|\.net|\.org|/', '', self.website)
        website_name = website_name.replace('.', '_')
        timestamp = int(datetime.now().timestamp())
        filename = f"{website_name}_{timestamp}"
        return filename

    def __generate_prompts(self):
        try:
            # Wait for the positive prompts text box to be visible and clickable
            positive_prompts_textbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, 'positivePrompts'))
            )
            positive_prompts_textbox.send_keys(f"cat_ears sfw {self.prompts}")

            # Wait for the negative prompts text box to be visible and clickable
            negative_prompts_textbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, 'negativePrompts'))
            )
            negative_prompts_textbox.send_keys('human_ears crotch panties nude nsfw')
            
            return True
        except Exception:
            return False
    '''
    def __select_model(self):
        try:
            # Find and select the first option from the "model" drop-down
            model_dropdown = Select(self.driver.find_element(By.NAME, 'model'))
            model_dropdown.select_by_index(3)
            return True
        except Exception:
            return False
    '''
    def __select_model(self):
        model_dropdown = Select(self.driver.find_element(By.NAME, 'model'))
        num_models = len(model_dropdown.options)
        favourite_models_order = [num_models - 2, num_models - 1] + list(range(num_models - 2))

        least_busy_index = -1
        least_busy_queue = float('inf')  # Initialise with a large value

        # Start with the last model and work backwards
        for index in favourite_models_order:
            model_dropdown.select_by_index(index)

            time.sleep(1)

            # Find the queue status element
            queue_status_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'flex items-center')]/p[contains(text(), 'Queue:')]")
            
            # Extract the queue number from the element
            queue_number = int(re.search(r"Queue: (\d+)", queue_status_element.text).group(1))

            # Check if the queue is less than or equal to 10
            if queue_number <= 10:
                return True  # Model selected successfully
            
            # Update least busy model if applicable
            if queue_number < least_busy_queue:
                least_busy_queue = queue_number
                least_busy_index = index

        # If no suitable model with queue <= 10 is found, select the least busy model
        if least_busy_index >= 0:
            model_dropdown.select_by_index(least_busy_index)
            return True

    def __click_generate_button(self):
        try:
            # Find and click the "Generate" button
            generate_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate')]")
            generate_button.click()
            return True
        except Exception:
            return False

    def __wait_for_javascript_injection(self):
        try:
            # Wait for the temporary element to disappear, indicating that the JavaScript injection is complete
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, "//*[@id='dummyElement']"))
            )
            return True
        except Exception:
            return False

    def __wait_for_image_generation(self):
        try:
            # Wait for the image to be generated and the src attribute to change
            self.__wait_for_image_change()
            return True
        except Exception:
            return False

    def __download_image_data(self):
        try:
            # Get the image data URL from the src attribute
            image_data_url = self.driver.find_element(By.XPATH, "//img[@alt='image']").get_attribute('src')

            # Inject JavaScript to extract the image data from the blob URL asynchronously
            image_data = self.driver.execute_script(f'''
                var xhr = new XMLHttpRequest();
                xhr.open('GET', "{image_data_url}", true);
                xhr.responseType = 'blob';
                xhr.onload = function () {{
                    var reader = new FileReader();
                    reader.readAsDataURL(xhr.response);
                    reader.onloadend = function () {{
                        var base64data = reader.result.split(',')[1];
                        window.imageData = base64data;
                    }};
                }};
                xhr.send();
            ''')

            # Wait for the JavaScript to complete
            time.sleep(5)

            # Get the image data from the window object
            image_data = self.driver.execute_script('return window.imageData')

            # Create the filename with the website name and timestamp
            filename = f"{self.__parse_filename()}.png"

            # Open the file with the filename and write the image data
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(image_data))

            return True
        except Exception:
            return False

        
    async def generate_and_download_image(self):
        if not self.driver:
            self.__start_browser()

        try:
            self.driver.get(self.website)

            # Wait for the page to be fully loaded
            if not self.__wait_for_page_to_load():
                return None

            # Add a temporary element to indicate that the JavaScript injection is about to happen
            self.driver.execute_script("var dummyElement = document.createElement('div');")

            # List of methods to execute sequentially
            methods_to_execute = (
                self.__generate_prompts,
                self.__select_model,
                self.__click_generate_button,
                self.__wait_for_javascript_injection,
                self.__wait_for_image_generation,
                self.__download_image_data
            )

            # Iterate through the methods and execute them
            for method in methods_to_execute:
                if not method():
                    return None

            # Get the filename
            filename = self.__parse_filename() + ".png"

            # Get the full path to the downloaded file
            full_path = os.path.join(os.getcwd(), filename)

            # Return the full path to the downloaded file
            return full_path, self.original_prompts

        except Exception:
            # If any error occurs, return None
            return None
        finally:
            # Don't forget to stop the browser when you are done
            self.__stop_browser()

'''
# Create an instance of the WaifuGenerator class
generator = WaifuGenerator(prompts=input("Prompts: "))

# Call the method to download the generated image and check the result
result = generator.generate_and_download_image()
#print(result)

if result:
    print("Image successfully generated and downloaded.")
else:
    print("Image generation timed out or encountered an error.")

# Don't forget to stop the browser when you are done
generator._WaifuGenerator__stop_browser()
'''
'''
async def main():
    # Create an instance of the WaifuGenerator class
    generator = WaifuGenerator(prompts=input("Prompts: "))

    # Call the asynchronous method using the 'await' keyword
    result = await generator.generate_and_download_image()
    print(result)

    if result:
        print("Image successfully generated and downloaded.")
    else:
        print("Image generation timed out or encountered an error.")

# Run the asynchronous function
asyncio.run(main())
'''