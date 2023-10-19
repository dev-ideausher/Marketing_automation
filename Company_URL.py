from apify_client import ApifyClient
import csv
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


API_KEY="api_key" #apify crunchbase scraper api

# Initialize the Apify client
client = ApifyClient(API_KEY)

def get_company_data(search_url):
# Prepare the Actor input
 run_input = {
    "action": "search",
    "search.url": search_url,
    "count": 1,
    "cursor": "",
    "minDelay": 1,
    "maxDelay": 3,
    "cookie":[
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1728734892.603135,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_delighted_web",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "{%220SrRdbRV9pdk0Aem%22:{%22_delighted_fst%22:{%22t%22:%221694168108944%22}%2C%22_delighted_lst%22:{%22t%22:%221694174892606%22%2C%22m%22:{%22token%22:%22ubPU8vJjstPDDageM0XPoRYN%22}}}}",
        "id": 1
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1704096549,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_fbp",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "fb.1.1694069552974.395410312",
        "id": 2
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1730880549.209565,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "GA1.2.1097320695.1694069551",
        "id": 3
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1730457471.387391,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_4N77WNB622",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "GS1.1.1695897455.6.1.1695897471.0.0.0",
        "id": 4
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1730880549.170194,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_97DKWJJNRK",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "GS1.1.1696318406.24.1.1696320549.48.0.0",
        "id": 5
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1730880549.178533,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_PGHC4BDGLM",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "GS1.1.1696318406.24.1.1696320549.0.0.0",
        "id": 6
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1703673469,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gac_UA-60854465-1",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "1.1695897469.CjwKCAjwyNSoBhA9EiwA5aYlb1f6nD437bdbkqq2Th0rXi0jDYVSMHjLHaWgPJm6wsitMYbrfTiKQRoCdmkQAvD_BwE",
        "id": 7
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1696320596,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gat_UA-60854465-1",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "1",
        "id": 8
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1701845550,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_au",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "1.1.227434627.1694069550",
        "id": 9
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1703673469,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_aw",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "GCL.1695897469.CjwKCAjwyNSoBhA9EiwA5aYlb1f6nD437bdbkqq2Th0rXi0jDYVSMHjLHaWgPJm6wsitMYbrfTiKQRoCdmkQAvD_BwE",
        "id": 10
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1696406949,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "GA1.2.271007871.1696318406",
        "id": 11
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1729975068,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_hp2_id.973801186",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "%7B%22userId%22%3A%222359928726902347%22%2C%22pageviewId%22%3A%2285274295080782%22%2C%22sessionId%22%3A%228358179453850224%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D",
        "id": 12
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1730457468.925665,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_mkto_trk",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "id:976-JJA-800&token:_mch-crunchbase.com-1694181204504-86623",
        "id": 13
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1696320877,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_px3",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "79e0d84224b439d341cf2aad7a9b6ca6b107c05694307bdfaeec3356d054503c:sKbsGcQ6f/mav8AY5TvXMQdskFxnW6Udh6M3z65UNjttFda+dcVhRJzeLwnBRgBJyBIu/XK5jwB9qSunPbpbbw==:1000:rBJFSrmeQEqpD9ruZBcgQsAegNncVHKNs+oG2kVGvlSEN55Ah8izFl9uYzaBV8P7m1qBGbFTSZEyzsd1F9ld3Vqg2sbSOOVLhiCR0DBMg/eog1qv+lGQFj9YCJUEse75d0s/JEuEw4NffyQnMGXglSlAXJd77ldli7JRN+m9LzsLmQQKO6W5QDWqxiqeRv6mbNj1uw5zhWPj/Jz8Rw4x0+/6rtB7rW0I0T3jmsiNVcY=",
        "id": 14
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1725605549,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_pxvid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "1c11bcde-4d4b-11ee-8061-a4e4a9359a23",
        "id": 15
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1696406947,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_uetsid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "2412091061bf11eea6459bddf17297aa",
        "id": 16
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1730016547,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_uetvid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "1d7c16a04d4b11ee9074c9cb6facc173",
        "id": 17
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1728629548.273097,
        "hostOnly": False,
        "httpOnly": False,
        "name": "cid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "CihgqWT5cysbwQAbIGVkAg==",
        "id": 18
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1696322349,
        "hostOnly": False,
        "httpOnly": False,
        "name": "fs_lua",
        "path": "/",
        "sameSite": "strict",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "1.1696320549697",
        "id": 19
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1725705756,
        "hostOnly": False,
        "httpOnly": False,
        "name": "fs_uid",
        "path": "/",
        "sameSite": "strict",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "#BA8KZ#7e8d19de-74a9-49a6-9ba0-0648665a94ff:ee63f97b-dc68-4d69-9142-061a06e18079:1696320549697::1#/1725705756",
        "id": 20
    },
    {
        "domain": ".crunchbase.com",
        "expirationDate": 1727856546,
        "hostOnly": False,
        "httpOnly": False,
        "name": "OptanonConsent",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "isGpcEnabled=0&datestamp=Tue+Oct+03+2023+13%3A39%3A06+GMT%2B0530+(India+Standard+Time)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=False&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=False",
        "id": 21
    },
    {
        "domain": ".crunchbase.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "pxcts",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "storeId": "0",
        "value": "4b1979b5-60e6-11ee-bc3c-a842c499ac73",
        "id": 22
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1696392527.628983,
        "hostOnly": True,
        "httpOnly": True,
        "name": "__cflb",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "02DiuJLCopmWEhtqNz4m5UYJ4QP8N5ierTk79h75YhjDv",
        "id": 23
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1727855536.975802,
        "hostOnly": True,
        "httpOnly": False,
        "name": "_pxhd",
        "path": "/",
        "sameSite": "unspecified",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "dWDYz34kva1v-BX0mI8XLwYDbXPGVtznOY9h7Lq/IjFbzW6NZ9MN/sYYeVpT-WEFoLiDfrtyYPde55oFKNQ0gg",
        "id": 24
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1711872343.284364,
        "hostOnly": True,
        "httpOnly": False,
        "name": "authcookie",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiJiMDQwNjBiYS1kNTMxLTRlNDktYWMwZS0yZGFhMGEyNDQyODIiLCJpc3MiOiJ1c2Vyc2VydmljZV84ODA1NmQ1Nl83MDgiLCJzdWIiOiI3MWZlZmNjMy1mMDIwLTQ1MWYtOTRhNS05OWUxZjRhZDBlNjIiLCJleHAiOjE2OTYzMjA2NDMsImlhdCI6MTY5NjMyMDM0MywicHJpdmF0ZSI6IlhBbVRTc2V5enVsWjVuRE5BTnlJOTBoQUxkVVRpSUJwSzBlTUFkTWNrdlhsZFVIN29GWDZPY3dDRi8rR0cvVTVVNisvNDRSb29uZm5EMEdXblE3K2paWlpwUnlhdTJWQThHS0RydHhteTlwOER3SGdWbjVld1hEaTlvWTZGaUEvNEczVG41ZnZxTVd0VDR1TDhUSjdaaVdPSmZJL3F4bjRxS0c2WmR5UnlUcVliSU1JL3ZaYllOTUZDR2Z4b1FjK2EvdExpeU1kWlVxNXlia3o3VjhSY1h0amJzTEZ4T1R5R0lsOGpqN2RnVGdQTGNrSWNSbndMY2IxS0NUVWJOOVhaZVZ6N3BkL1c2RzJIdFJzdThmRlEyTC9FQkh2cXpBd2RWVHJObnA1ZEpzWE9wMm0rSG9obUNBY3JiRWM3OXZXcllhaWVEdENmWWk5bWlYUUlXOEp6L0IweDh6UlBCQnk2YktCV2xrTHU0S0RhNTA1d1dkeDlVS3pCWmswN0dSNFUwY29CUzNNbFpLeU9WNDVvbzF0Z0Q0eERVUkl1SlNRM2k3ZEFHcFZTNWhEa0dvTXRUbm1DQ2xZLzYwclNkc252WXRLa0NKcjFpaGx4cXZJQkF6b0tlUHpDNE9LSllncVFHRTQyeE05VkVML1UzSzBUb2dUQUtxdXlBQWJpdHRjWTdLYWRDN2d0KzNRRk16aDUwTVMwODhsQ3lqR2ZKS21pMEwyWnd4OXhVVXFaR1Q2OGVlbVozUUJFVWpucEpheG5sWFhUYStTRDgzWXNOdkxvbVJ2bnJrTGRoYU1GS0V3MHpVNVF3eTFDUTVLRTVJUHd2M1BuT0dQL0VQVkg1Uk0yNkVJYkxodVc0L3RqQmpmZFhQTjJmMTlrdEhXRHFFdk9qUFFET1Y1dUNXSW84SHB2WGlxSU9VZElOZmViZTAyVlhYNk80NTJwaXFxUTZEL1lOc0dpeUFPM01FaFk3ZGFuRkQ1d2Y3R3RuUU5nWnR0QUlBYnJlNStoS0p0U2ZkTHJJWTZ1ak9sdGFQYkxBKy95UC9iSGJQMVdRLzZ1REZUWlZ5R0M0OVJyMVhBQ2lLYjlpOTlXM1pxVmdwS2NPenpNcFF6Q1VYKzFmaUdtRUNUQUdLb2V6ODFCZzRPK20vRlBxVWlaUFVpZVBIU0NJc1pDc29WajhndXlsUFlBTURwWnlnRTlGTnZYODFPbkZCV0JTRGZyOXhKK2dWQ3pqYTZPdWRZbXY4RFpYTXlDZFFySDRMT0pmZElHTzNkTDhqV0oyUXVqc3Zhd3R0b0hqUFFJSWJIcVQ5c0NPdFlmS1p6cHM5ZmZHNnFWMy9YcFBVZEwzRWZxYnBqczU3S2lnTmpaOEdUZEhzMnRyVnpVQ0ErMjdoR1F3SVdMRmRCdGNGWFNrZldzNUNEckJubUN0U1g4Rm9Za2hSZ2diaXVGK2RKQldlc0hGaHFlbXBJaGY3K1dQK0dXZmhwRzJ4YkIvVFdDNjdwNmFFbXlhMHA0TTF1dnNzVzNkbEhnTmF4MERpMHEyVnByeFdST09paGZZbzVCRU0zYzJyd0VudXpyWVk2TU5yNUZxNWJMa2ttemJ6b1M4dVlBbU9qV1U1cDI4SEdGSHk3UEwvMzFpQjFYZFdCZXlqZnBNemtSdlphMHIrYllNRmhGbW5iYXl6cGRVNnU0RGc5dmswUWV6RXd5Y3pYIiwicHVibGljIjp7InNlc3Npb25faGFzaCI6IjIwNTg0NTE3NjYifX0.TwueYZZmcEQphqTtnmvZr-5kxhgEv8qUEwYPSV9BYGMihRC5dCM_P2E4KHEAtHhMFobC32ondOKfddJHw6GF9Q",
        "id": 25
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1727942946,
        "hostOnly": True,
        "httpOnly": False,
        "name": "cb_analytics_consent",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "granted",
        "id": 26
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1728715265.860028,
        "hostOnly": True,
        "httpOnly": False,
        "name": "drift_aid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "736bf12f-5ac0-47c1-8feb-5c70c04d64e8",
        "id": 27
    },
    {
        "domain": "www.crunchbase.com",
        "hostOnly": True,
        "httpOnly": False,
        "name": "drift_eid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": True,
        "session": True,
        "storeId": "0",
        "value": "71fefcc3-f020-451f-94a5-99e1f4ad0e62",
        "id": 28
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1728715265.861472,
        "hostOnly": True,
        "httpOnly": False,
        "name": "driftt_aid",
        "path": "/",
        "sameSite": "unspecified",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "736bf12f-5ac0-47c1-8feb-5c70c04d64e8",
        "id": 29
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1730880546.77967,
        "hostOnly": True,
        "httpOnly": False,
        "name": "featureFlagOverride",
        "path": "/",
        "sameSite": "lax",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "%7B%7D",
        "id": 30
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1730880546.779893,
        "hostOnly": True,
        "httpOnly": False,
        "name": "featureFlagOverrideCrossSite",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "%7B%7D",
        "id": 31
    },
    {
        "domain": "www.crunchbase.com",
        "expirationDate": 1696404806,
        "hostOnly": True,
        "httpOnly": False,
        "name": "ln_or",
        "path": "/",
        "sameSite": "unspecified",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "eyIzOTYwMzYiOiJkIn0%3D",
        "id": 32
    },
    {
        "domain": "www.crunchbase.com",
        "hostOnly": True,
        "httpOnly": False,
        "name": "xsrf_token",
        "path": "/",
        "sameSite": "strict",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "jgu3SrNbRnRidZAjNWkvIj8PulWLeBoK/IIa2dMrzzA=",
        "id": 33
    }
]
}

 extracted_data=[]
 run = client.actor("curious_coder~crunchbase-scraper").call(run_input=run_input)

 for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    company_name = item.get('name', '')
    company_website = item.get('website', {}).get('value', '')
    short_description = item.get('short_description', '')
    email = item.get('contact_email', '')
    phone_no = item.get('phone_number', '')  
    linkedin = item.get('linkedin', {}).get('value', '')
    
    extracted_data.append([company_name, company_website, short_description, email, phone_no, linkedin])

 scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
 credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/shal1/OneDrive/Desktop/extra/pr/marketing-automations-401806-124a6a502fd9.json', scope)
 gc = gspread.authorize(credentials)
 spreadsheet = gc.open('Automated_Data')
 worksheet = spreadsheet.worksheet('Sheet1')

 header = ['Company Name', 'Company Website', 'Short Description', 'Company Email', 'Company Phone Number', 'Company LinkedIn']

 existing_header = worksheet.row_values(1)
 if existing_header:
    worksheet.update('A1:F1', [header])
 else:
    worksheet.insert_row(header, 1)


 for data in extracted_data:
    worksheet.append_row(data)

 print("Company Data has been written to Google Sheets.")

# search_url="https://www.crunchbase.com/discover/organization.companies/367783e4846403878242ec84eee33d5b"
# get_company_data(search_url)