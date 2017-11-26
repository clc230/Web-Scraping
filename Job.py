import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.indeed.com/jobs?q=data+analyst&l=Cleveland"
# conducting a request of the stated URL above:
page = requests.get(URL)
# specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
soup = BeautifulSoup(page.text, 'html.parser')
# printing soup in a more structured tree format that makes for easier reading
print(soup.prettify())

def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name='div', attrs={'class': 'row'}):
        for a in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
            jobs.append(a['title'])
    print(jobs)
    return jobs

extract_job_title_from_result(soup)

def extract_company_from_result(soup):
    comp = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        nameof = div.find_all(name='span', attrs={'class':'company'})
        if len(nameof) > 0:
            for b in nameof:
                comp.append((b.text.strip()))
        else:
            sec_try = div.find_all(name='span', attrs = {'class':'result-link-source'})
            for span in sec_try:
                comp.append(span.text.strip())
    print(comp)
    return comp
extract_company_from_result(soup)


def extract_summary_from_result(soup):
    summaries = []
    spans = soup.findAll('span', attrs={'class': 'summary'})
    for span in spans:
        summaries.append(span.text.strip())
    print(summaries)
    return(summaries)
extract_summary_from_result(soup)

max_results_per_city = 1000
columns = ['job_title', 'company_name', 'summary']
sample_df = pd.DataFrame(columns=columns)

for start in range(0, max_results_per_city, 10):
    page = requests.get('https://www.indeed.com/jobs?q=Data%20Python&l=Cleveland%2C%20OH' + '&start=' + str(start))
    time.sleep(1)  #ensuring at least 1 second between page grabs
    soup = BeautifulSoup(page.text, 'lxml', from_encoding='utf-8')
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        #specifying row num for index of job posting in dataframe
        num = (len(sample_df) + 1)
        #creating an empty list to hold the data for each posting
        job_post = []
        for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
            job_post.append(a['title'])
        #grabbing company name
        company = div.find_all(name='span', attrs={'class':'company'})
        if len(company) > 0:
            for b in company:
                job_post.append(b.text.strip())
        else:
            sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
            for span in sec_try:
                job_post.append(span.text)
        #grabbing summary text
        d = div.findAll('span', attrs={'class': 'summary'})
        for span in d:
            job_post.append(span.text.strip())
        #appending list of job post info to dataframe at index num
        print(job_post)
        sample_df.loc[num] = job_post

#saving sample_df as a local csv file — define your own local path to save contents
sample_df.to_csv('jobscientist.csv', encoding='utf-8')