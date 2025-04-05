from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from twilio.rest import Client


driver = webdriver.Chrome()


rcb_tickets_page_url = 'https://shop.royalchallengers.com/ticket'

tickets_date = "2025-05-03"
num_retry = 0
num_of_messages_to_send = 2  # Number of notification messages to send once tickets are available
interval_between_messages = 120  # Seconds between each notification message

# Twilio account details for sending SMS
account_sid = 'AC391334582646ead1ebb4a8ed6f388748'  # Twilio account SID
auth_token = 'efa5737569565941f6bb8c4e41c44aeb'  # Twilio auth token
client = Client(account_sid, auth_token)  # Twilio client initialization
twilio_contact_number = "+15075193300"  # Twilio phone number used for sending SMS
recipient_contact_number = "+917975007767" 
# recipient_contact_number_sandy = "+917353257355"
# recipient_contact_number_shash = "+918147414719"


# Script execution control variables
tickets_available = False  # Flag to track ticket availability status
sent_messages_count = 0  # Counter for messages sent
fetch_status_delay = 120  # Delay in seconds for script re-execution if tickets are not available


def twilio_call():
                for message_num in range(num_of_messages_to_send):
                    message = client.messages.create(
                        from_=twilio_contact_number,
                        body=f'The match tickets for CSK_v_RCB on {tickets_date} are available. Login to {rcb_tickets_page_url} to book the tickets immediately.',
                        to=recipient_contact_number
                    )
                    # message = client.messages.create(
                    #     from_=twilio_contact_number,
                    #     body=f'The match tickets for CSK_v_RCB on {tickets_date} are available. Login to {rcb_tickets_page_url} to book the tickets immediately.',
                    #     to=recipient_contact_number_shash
                    # )
                    # message = client.messages.create(
                    #     from_=twilio_contact_number,
                    #     body=f'The match tickets for CSK_v_RCB on {tickets_date} are available. Login to {rcb_tickets_page_url} to book the tickets immediately.',
                    #     to=recipient_contact_number_sandy
                    # )
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Message sent successfully - {message_num + 1} time(s)")
                    sent_messages_count += 1

                    if sent_messages_count == num_of_messages_to_send:
                        break

                    time.sleep(interval_between_messages)

                


def getPage(rcb_tickets_page_url):
    try:
    # Open the URL
        
        driver.get(rcb_tickets_page_url)

        # Allow time for JavaScript to load
        time.sleep(5)

        # Locate the div using ID
        rcb_shop_div = driver.find_element(By.ID, 'rcb-shop')

        # Print the content inside the div
        # print("Div Content Found!")

        # Extract all paragraph texts
        paragraphs = rcb_shop_div.find_elements(By.TAG_NAME, 'p')
        for p in paragraphs:
            # print("Paragraph:", p.text)
            try:
                # Try converting to a date
                date_obj = datetime.strptime(p.text, "%a, %b %d, %Y %I:%M %p")
                # print(str(date_obj.date()))
                formatted_date = str(date_obj.date()) 
                return True
                
            except ValueError:
                # Check if 'Chennai' is in the text
                if "Chennai" in p.text:
                    # print("Chennai Not Found")
                    pass
                    # return "Chennai Found"
                # return p.text
            # date_str = p.text
            # date_obj = datetime.strptime(date_str, "%a, %b %d, %Y %I:%M %p")
            # date_only = date_obj.date()

            # print(date_only)

        # # Extract all links
        # links = rcb_shop_div.find_elements(By.TAG_NAME, 'a')
        # for link in links:
        #     print("Link Text:", link.text)
        #     print("Link URL:", link.get_attribute('href'))

        # # Extract all images
        # images = rcb_shop_div.find_elements(By.TAG_NAME, 'img')
        # for img in images:
        #     print("Image Source:", img.get_attribute('src'))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

while not tickets_available:
    tickets_validation = getPage(rcb_tickets_page_url)
    
    if not tickets_available:
                    num_retry += 1
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Tickets not available. Retrying in {fetch_status_delay} seconds...\n num_of retries-->{num_retry}")
                    time.sleep(fetch_status_delay)
    else:
          twilio_call()