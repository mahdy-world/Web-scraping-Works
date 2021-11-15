import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
job_skill = []
job_location = []
links = []
responsibilites = []
date = []
page_number = 0

while True:
    
    # 2nd step use requests to fetch the url 
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python%20developer%20&start={page_number}")

        # 3rd step save page content/markup
        src = result.content

        # 4th step create soup object ot parse content 
        soup = BeautifulSoup(src , "lxml")
        page_limit = int(soup.find("strong").text)
        print(page_limit)
        
        # // this int devsion
        if( page_number > page_limit //40):
            print("pages ended")
            break
        
        
        # 5th step find the elements containing info you need 
        #-- job titles , job skills , company names , locations names 
        job_titles = soup.find_all("h2" , {"class":"css-m604qf"} )
        company_names = soup.find_all("a" , {"class" : "css-17s97q8"})
        jobs_skills = soup.find_all("div" , {"class":"css-y4udm8"})
        jobs_locations = soup.find_all("div" , {"class":"css-d7j1kk"})
        new_date = soup.find_all("div" , {"class":"css-4c4ojb"})
        old_date = soup.find_all("div" , {"class":"css-do6t5g"})
        posted_date = [*old_date , *new_date]
        

        # 6th step loop over returned lists to extract needed info into other lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            job_skill.append(jobs_skills[i].text)
            job_location.append(jobs_locations[i].text)
            date_text = posted_date[i].text.replace("-" ,"").strip() # strip means delete all spaces 
            date.append(date_text)
            
        page_number += 1
        print("page switched")  
          
    except:
        print("error")
        break
# loop over jobs details page 
for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src , "lxml")
    requerments = soup.find("div" , {"class":"css-1t5f0fr"}).ul
    print(requerments)
    respons_text = ""
    
for li in requerments.find_all("li"):
    respons_text += li.text+"| "
respons_text = respons_text[:-2]    
responsibilites.append(respons_text)       
    
    
# 7th step create csv file and fill it with values
file_list = [job_title, company_name, date, job_location, job_skill, links, responsibilites]
exported = zip_longest(*file_list)

with open("E:\My Work\Web Scraping\Jobs\jobstest.csv" , "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["job title", "compnay name", "date", "location",  "skills", "links", "requerments"])
    wr.writerows(exported)

