# import asyncio
# from playwright.async_api import async_playwright

# async def run(prompt):
#     async with async_playwright() as playwright:
#         browser = await playwright.chromium.launch(headless=False, args=['--disable-gpu'])
#         page = await browser.new_page()
#         url = "https://chatgpt.com"
#         await page.goto(url)

#                 # Wait for the textarea and button to be available without requiring them to be visible
#         await page.wait_for_selector("xpath=//*[@id='prompt-textarea']", state='attached')
#         await page.wait_for_selector("xpath=//*[@id='__next']/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/button", state='attached')
        
#         textarea = await page.query_selector("xpath=//*[@id='prompt-textarea']")
#         button = await page.query_selector("xpath=//*[@id='__next']/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/button")

#         # Fill textarea, click button, and wait for the response
#         await textarea.fill(prompt)
#         await asyncio.sleep(1)
#         await button.click()
#         await page.query_selector("xpath=//*[@id='__next']/div[1]/div[2]/main/div[2]/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div/span/button")

#         all_elements = await page.query_selector_all(".markdown.prose.w-full.break-words")
#         last_element = all_elements[-1]
        
#         paragraphs = await last_element.query_selector_all('p')
#         paragraph_texts = [await para.text_content() for para in paragraphs]

#         await browser.close()
#         return paragraph_texts
    
import asyncio
from playwright.async_api import async_playwright

async def run(prompt):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        url = "https://chatgpt.com"
        await page.goto(url)
        
        # Wait for the textarea to appear
        await page.wait_for_selector("xpath=//*[@id='prompt-textarea']", state='attached')
        textarea = await page.query_selector("xpath=//*[@id='prompt-textarea']")
        
        # Wait for the button to appear
        await page.wait_for_selector("xpath=//*[@id='__next']/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/button", state='attached')
        button = await page.query_selector("xpath=//*[@id='__next']/div[1]/div[2]/main/div[2]/div[2]/div[1]/div/form/div/div[2]/div/button")

        # Fill textarea, click button, and wait for the response
        await textarea.fill(prompt)
        await asyncio.sleep(1)
        await button.click()
        await page.wait_for_selector("xpath=//*[@id='__next']/div[1]/div[2]/main/div[2]/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div/span/button")

        all_elements = await page.query_selector_all(".markdown.prose.w-full.break-words")
        last_element = all_elements[-1]
        
        paragraphs = await last_element.query_selector_all('p')
        paragraph_texts = [await para.text_content() for para in paragraphs]

        await browser.close()
        return paragraph_texts