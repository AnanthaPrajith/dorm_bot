from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Target URL
URL = "https://www.stwdo.de/wohnen/aktuelle-wohnangebote"

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(URL)

# Get page source
html = driver.page_source
driver.quit()

# Parse HTML
soup = BeautifulSoup(html, "html.parser")
offers_div = soup.find("div", class_="section mt-4 mb-4")

# Check if "KEINE ANGEBOTE" is shown
if offers_div and "NO OFFERS" in offers_div.text.upper():
    print("❌ No dorms available – no email sent.")
else:
    print("✅ Dorm offer found – sending email.")

    # Email setup
    EMAIL_SENDER = "ananthaprajith7kct@gmail.com"
    EMAIL_PASSWORD = "ltyf okjk iulv lqeb"
    EMAIL_RECEIVER = "d97227704@gmail.com"

    subject = "🏠 Dorm Available!"
    body = f"A new dorm listing has been posted!\n\nCheck it out: {URL}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
