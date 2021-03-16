import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
def extract(page):
    headers = {
        "User=Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    url = f"https://uk.indeed.com/jobs?q=python+developer&l=London&start={page}"
    site = requests.get(url, headers)
    soup = BeautifulSoup(site.text, "html.parser")
    return soup


def transform(soup):
    time.sleep(2)
    divs = soup.find_all("div", class_="jobsearch-SerpJobCard")
    for item in divs:
        title = item.find("a").text.strip()
        link = item.find("a")["href"]
        company = item.find("span", class_="company").text.strip()
        location = item.find("span", class_="location").text.strip()
        try:
            salary = item.find("span", class_="salaryText").text.strip()
        except:
            salary = ""
        summary = item.find("div", class_="summary").text.strip().replace("\n", "")
        #  summary = item.find("div", {"class" : "summary"}).text.strip() can be done like this too...
        #  for class, dict, anything {attribute : value}
        job = {
            "title": title,
            "link": link,
            "company": company,
            "location": location,
        }
        job_list.append(job)

job_list = []
for i in range(0, 40, 10):
    print(f"getting page,", {i})
    c = extract(i)
    transform(c)
df = pd.DataFrame(job_list)
print(df.head())
df.to_csv("jobs", index=False)

