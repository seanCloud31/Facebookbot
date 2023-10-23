import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import time
import json

# Define your account credentials and other settings
#account = {"username": "sv0985797@gmail.com", "password": "SeanUpwork@3131", "profile": "Assistance Help","code":"44RE KX7P OFJK 5AIV WKPV 4XX5 5JC2 WIMN"}
#account = {"username": "ggnjrhqv@firstmailler.net", "password": "V4RBCYDD", "profile": "PoIicy VioIation","code":"CHMUXBN7ABFOH6YLLETDUOUEJBCYJE3N"}
account = {"username": "osdtgdew@firstmailler.com", "password": "SO0O1CHF", "profile": "PoIicy VioIation Message","code":"ACE2AOSAZV7UVTLFU3AWS4NOFBXPQQSP"}
message = "Hi How are you\n Hope you are doing good"


csvName = "linksofpages.csv"
batchLimit = 20
waitTime = 0
messageLimit = 10000 # Change account after sending this many messages

data = pd.read_csv(csvName, header=None)
data.columns = ['page_name']
pages = list(data['page_name'])

'''
with open("links.json") as f:
    d = json.load(f)
pages= d["links"]
print(len(pages))
'''
async def send_message(context, link, message, account):
    try:
        page = await context.new_page()
        await page.goto(link)

        # Ensure that the "Message" button is present before clicking
        await page.wait_for_selector('[aria-label="Message"]', timeout=10000)
        await page.get_by_label("Message").click()

        # Click on the message text box and send the message
        await page.get_by_role("textbox", name="Send a message as " + account["profile"]).click()
        await page.get_by_role("textbox", name="Send a message as " + account["profile"]).clear()
        await page.get_by_role("textbox", name="Send a message as " + account["profile"]).fill(message)
        await page.get_by_label("Send Message").click()
        await asyncio.sleep(waitTime)
        await page.close()
        return  # Successful message sent

    except Exception as e:
        print(f"Error sending message on {link}: {str(e)}")
        await page.close()  # Close the page if an error occurs
        return


async def main():
    async with async_playwright() as p:
        # Initialize message count
        message_count = 0

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Launch browser and log in using the current account

        # Set the max waiting time for loading a page
        context.set_default_timeout(60000)
        page = await context.new_page()
        await page.goto("https://www.facebook.com/")

        # Log in
        await page.get_by_test_id("royal_email").click()
        await page.get_by_test_id("royal_email").fill(account["username"])
        await page.get_by_test_id("royal_pass").click()
        await page.get_by_test_id("royal_pass").fill(account["password"])
        await page.get_by_test_id("royal_login_button").click()

        page1 = await context.new_page()
        await page1.goto("https://2fa.live/")
        await page1.get_by_placeholder("BK5V TVQ7 D2RB...").click()
        await page1.get_by_placeholder("BK5V TVQ7 D2RB...").fill(account["code"])
        await page1.get_by_text("Submit").click()
        time.sleep(2)
        element = page1.locator('[placeholder="ABC|2FA Code"]')

        # Get the value of the element using page.evaluate
        code = await element.evaluate('(element) => element.value')
       #code  = await page1.locator('[placeholder="ABC|2FA Code"]').value()
        print(code)
        idValue = code.split("|")[1]
        await page.get_by_placeholder("Login code").click()
        await page.screenshot(path='example.png')
        await page.get_by_placeholder("Login code").fill(idValue)
        await page.screenshot(path='example1.png')
        await page.get_by_role("button", name="Submit code").click()
        await page.get_by_role("button", name="Continue").click()
        try:
            await page.get_by_role("button", name="Continue").click()
            await page.get_by_role("button", name="This was me").click()
            await page.screenshot(path='example4.png')
            await page.get_by_role("button", name="Continue").click()
        except:
            print("new login")
            await page.screenshot(path='example3.png')

        await page.screenshot(path='example.png')
        # Change profile
        await page.wait_for_selector('[aria-label="Your profile"]')
        await page.get_by_role("button", name="Your profile").click()
        try:
            try:
                await page.get_by_label("Switch", exact=True).click()
                await page.screenshot(path='exampledesign1.png')
                await page.get_by_role("radio", name=account["profile"]).click()
            except:
                await page.get_by_label("Switch Profiles").click()
        except:
            await page.get_by_role("button", name="Switch Profiles "+account["profile"]).click()
            await page.screenshot(path='exampledesign2.png')

        while message_count<=messageLimit and message_count<len(pages):
            # Send messages using the current account
            message_start_index = message_count
            message_end_index = min(message_count + batchLimit, len(pages))
            pageBatch = pages[message_start_index:message_end_index]

            tasks = [send_message(context, link, message, account) for link in pageBatch]
            await asyncio.gather(*tasks)

            # Update message count
            message_count += len(pageBatch)

        # Save remaining pages to CSV file
        remaining_pages = pages[message_count:]
        if remaining_pages:
            remaining_data = pd.DataFrame({'page_name': remaining_pages})
            remaining_data.to_csv(csvName, index=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {str(e)}")
