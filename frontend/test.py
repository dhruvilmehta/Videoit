import requests
from bs4 import BeautifulSoup
import urllib.parse

# proxyUrl="http://43.135.180.61:13001"
# proxies={
#     "http": proxyUrl,
#     "https": proxyUrl
# }
response = requests.get("https://www.linkedin.com/jobs/search/?currentJobId=4214799359&f_E=2&f_TPR=r300&geoId=103644278&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")

# print("Response", response.content)
soup = BeautifulSoup(response.content, 'html.parser')
a_tags = soup.find_all('a', class_='base-card__full-link')

divs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

job_posting_ids = []

for div in divs:
    entity_urn = div.get('data-entity-urn')
    if entity_urn:
        job_id = entity_urn.split(':')[-1]
        job_posting_ids.append(job_id)

hrefs = [a['href'] for a in a_tags if a.get('href')]

print(len(hrefs), len(job_posting_ids))

seen_ids_file = "seen_ids.txt"
seen_ids = set()
try:
    with open(seen_ids_file, 'r', encoding='utf-8') as f:
        seen_ids = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    pass

seen_ids_file = open(seen_ids_file, 'a', encoding='utf-8')
file=open("output.txt", "w", encoding="utf-8")
soup1=None
for i in range(0, min(100, len(hrefs))):
    if job_posting_ids[i] in seen_ids:
        print("ID already seen, skipping:", job_posting_ids[i])
        continue
    
    print("Writing to file")
    response1=requests.get(hrefs[i])
    soup1=BeautifulSoup(response1.content, 'html.parser')
    
    element = soup1.find(id='applyUrl')
    timeElement=soup1.find(class_="posted-time-ago__text")
    time=str(timeElement.contents[0]).strip()
    
    titleElement=soup1.find(class_="top-card-layout__title")
    title=str(titleElement.contents[0]).strip()
    # print("Title Element", title)
    # print("Time Element", time)
    
    company=soup1.title.string
    # print("Company", company)
    if not element:
        file.write("Easy Apply\n")
        file.write(f"Title {title}\n")
        file.write(f"{company}\n")
        file.write(f"Time {time}\n")
        file.write(hrefs[i])
        file.write("\n")
        file.write("\n")
        
        seen_ids_file.write(job_posting_ids[i]+'\n')
        continue
    # print("Element", element)
    # print("Text", element.contents[0])
    url=element.contents[0]
    parsedUrl=urllib.parse.urlparse(url)
    queryParams=urllib.parse.parse_qs(parsedUrl.query)
    # print("Query Params", queryParams.get('url')[0])
    file.write(f"Time {time}\n")
    file.write(f"Title {title}\n")
    file.write(f"{company}\n")
    file.write(str(queryParams.get('url')[0]))
    file.write('\n')
    file.write('\n')
    seen_ids_file.write(job_posting_ids[i]+'\n')

if soup1:
    file=open("output1.html", "w", encoding="utf-8")
    file.write(soup1.prettify())

# print(soup.prettify())
file = open("output.html", "w", encoding="utf-8")
file.write(soup.prettify())
file.close()
