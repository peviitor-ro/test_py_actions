from scraper_peviitor import Scraper, loadingData
import uuid
import json

apiUrl = "https://refinitiv.wd3.myworkdayjobs.com/wday/cxs/refinitiv/Careers/jobs"

company = {"company": "LSEG"}
finalJobs = list()

scraper = Scraper()

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

data = {"appliedFacets":{"locationCountry":["f2e609fe92974a55a05fc1cdc2852122"]},"limit":20,"offset":0,"searchText":""}

scraper.session.headers.update(headers)

numberOfJobs = scraper.post(apiUrl, json=data).json().get("total")

iteration = [i for i in range(0, numberOfJobs, 20)]

for num in iteration:
    data["offset"] = num
    jobs = scraper.post(apiUrl, json=data).json().get("jobPostings")
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.get("title")
        job_link = "https://refinitiv.wd3.myworkdayjobs.com/en-US/Careers" + job.get("externalPath")
        country = "Romania"
        city = job.get("locationsText").split(",")[0]

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": country,
            "city": city
        })

        print(job_title + " -> " + city)

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-Tp_lBl4hy9WFitdNzAtRw2tgxLYnxf1lyNrnXx8h&s"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))
        