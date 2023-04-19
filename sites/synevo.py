from scraper_peviitor import Scraper, Rules, loadingData
import uuid

#Cream o instanta a clasei Scraper
scraper = Scraper("https://www.synevo.ro/cariere/")
rules = Rules(scraper)

#Luam toate categoriile de joburi
jobsCategory = rules.getTags("div", {"class": "job-cat-post"})

finaljobs = list()

#Pentru fiecare categorie de joburi luam linkul si mergem pe pagina
for jobCategory in jobsCategory:
    #Luam linkul categoriei de joburi
    jobCategoryLink = jobCategory.find("a")["href"]
    #Mergem pe pagina categoriei de joburi
    scraper.url = jobCategoryLink

    #Luam toate joburile din categoria respectiva
    job_link = rules.getTags("a", {"class": "jobs-link"})

    for job in job_link:
        #Mergem pe pagina jobului
        scraper.url = job["href"]
        #Luam titlul jobului si orasele in care se poate lucra
        job_title = rules.getTag("h1", {"class": "entry-title"}).text
        #Daca sunt mai multe orase le impartim in lista
        try :
            citys = rules.getTag("div", {"class": "jobs-info-city"}).find("b").text.split(",")
        except:
            citys = [rules.getTag("div", {"class": "jobs-info-city"}).find("b").text]
        print(job_title + " -> " + citys[0])

        #Cream un dictionar cu jobul si il adaugam in lista finala
        for city in citys:
            job = {
                "id": str(uuid.uuid4()),
                "job_title": job_title,
                "job_link": scraper.url,
                "company": "Synevo",
                "country": "Romania",
                "city": city.strip(),
            }
            finaljobs.append(job)

#Afisam numarul total de joburi
print("Total jobs: " + str(len(finaljobs)))

#Incarcam datele in baza de date
loadingData(finaljobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", "Synevo")
