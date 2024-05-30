import asyncio
from time import sleep
from playwright.async_api import async_playwright

async def block_ads(route, request):
    # List of common ad-serving domains
    ad_domains = [
        "doubleclick.net",
        "googleadservices.com",
        # Add more ad-serving domains as needed
    ]

    for domain in ad_domains:
        if domain in request.url:
            await route.abort()
            return

    await route.continue_()

async def run(prompt):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await context.new_page()
        await page.route("**/*", block_ads)
        await page.goto("https://deepai.org/chat", timeout=60000)

        stoppers = ["exit", "stop", "quit", "abort"]
        while prompt.lower() not in stoppers and prompt:
            textarea = await page.query_selector("textarea[placeholder='Chat with AI...']")
            button = await page.query_selector("#chatSubmitButton")

            await textarea.fill(prompt)
            await button.click()
            await asyncio.sleep(5)

            containers = await page.query_selector_all(".outputBox")
            container = containers[-1]
            paragraphs = await container.query_selector_all("p")
            paragraph_texts = [await para.text_content() for para in paragraphs]
            return paragraph_texts

        await browser.close()
        return ["chat stopped"]