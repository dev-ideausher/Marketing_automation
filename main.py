import Company_URL as C
import People_URL as P
import ContactData as CD




if __name__=="__main__":
    search_url="https://www.crunchbase.com/discover/organization.companies/367783e4846403878242ec84eee33d5b"
    C.get_company_data(search_url)
    P.get_people_url()
    CD.get_contact_data()