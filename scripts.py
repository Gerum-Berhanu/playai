import os
import asyncio

def screenshot_path(path=""):
    check = 0
    org_path = path
    expt_path = path
    while os.path.exists(expt_path):
        img_split = org_path.rsplit(".", 1)
        expt_path = img_split[0] + f"-{check}." + img_split[-1]
        check += 1
    return expt_path

async def screen_capture(page, path, full_page=False):
    await page.screenshot(path=screenshot_path(path), full_page=full_page)