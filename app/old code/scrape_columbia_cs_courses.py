
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_columbia_cs_courses():
    url = "https://www.cs.columbia.edu/education/undergrad/courses/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all course blocks
    course_blocks = soup.select(".course")  # This class may vary depending on the actual HTML structure

    courses = []

    for block in course_blocks:
        title_elem = block.find("h3")
        desc_elem = block.find("p")

        if title_elem and desc_elem:
            title = title_elem.get_text(strip=True)
            desc = desc_elem.get_text(strip=True)
            courses.append({"Title": title, "Description": desc})

    df = pd.DataFrame(courses)
    df.to_csv("columbia_cs_courses.csv", index=False)
    print(f"✅ Scraped {len(df)} courses and saved to columbia_cs_courses.csv")

if __name__ == "__main__":
    scrape_columbia_cs_courses()
