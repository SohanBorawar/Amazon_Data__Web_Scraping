from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Product Url
def get_url(soup):
    try:
        
        producturl = soup.find("link", attrs={"rel": "canonical"})

        
        producturl_string = producturl.get("href").strip()

    except AttributeError:
        producturl_string = ""

    return producturl_string

# Function to extract Product Rating
def get_review_count(soup):

    try:
        review_count = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            review_count = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            review_count = ""	

    return review_count    


# Function to extract Number of User Reviews
def get_rating(soup):
    try:
        rating = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        rating = ""	

    return rating


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available

# Function to extract Product Title
def get_title(soup):

    try:
        
        title = soup.find("span", attrs={"id":'productTitle'})
        
        
        title_value = title.text

        
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={"class":"a-offscreen"}).string.strip()

    except AttributeError:

        try:
            
            price = soup.find("span", attrs={"class":"a-offscreen"}).string.strip()

        except:
            price = ""

    return price


# Function to extract Asin
def get_asin(soup):

    try:
        
        asin = soup.find("input",attrs={"name":"ASIN"})

        
        asin_string = asin.get("value").strip()

    except:
        asin_string = ""

    return asin_string        

# Function to extract Product Description
def get_productdescription(soup):

    try:
        description = soup.find("div", attrs={'id':"productDescription"})
        description = description.find("span").string.strip()

    except AttributeError:
        description = "No Description"	

    return description


# Function to extract Manufacturer
def get_Manufacturer(soup):
    try:
        
        Manufacturer = soup.find("a", attrs={'id':'bylineInfo'})
        
        
        Manufacturer_value = Manufacturer.text

        
        Manufacturer_string = Manufacturer_value.strip()

    except AttributeError:
        Manufacturer_string = ""

    return Manufacturer_string

if __name__ == '__main__':

    
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

    # Number Of Pages To Get Product
    num_pages = 20
    page_urls = []
    for page in range(1,num_pages+1):
        URL = base_url + f'&page={page}'
        page_urls.append(URL)


    d = {'Product URL':[], 'Product Name':[], 'Product Price':[], 'Rating':[], 'Number of Reviews':[],
                    'availability':[], 'ASIN':[], 'Product Description':[], 'Manufacturer':[]}

    for linkpage in page_urls:
        print(linkpage)
        print("*"*60)
        
        # HTTP Request
        webpage = requests.get(linkpage, headers=HEADERS)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        # Store the links
        links_list = []

        # Loop for extracting links from Tag Objects
        for link in links:
                links_list.append(link.get('href'))

        
        
        # Loop for extracting product details from each link 
        for link in links_list:
            if str(link).startswith('https'):                

                new_webpage = requests.get(link, headers=HEADERS)

                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        
                # Function calls to display all necessary product information
                d['Product URL'].append(get_url(new_soup))
                d['Product Name'].append(get_title(new_soup))
                d['Product Price'].append(get_price(new_soup))
                d['Rating'].append(get_rating(new_soup))
                d['Number of Reviews'].append(get_review_count(new_soup))
                d['availability'].append(get_availability(new_soup))
                d['ASIN'].append(get_asin(new_soup))
                d['Product Description'].append(get_productdescription(new_soup))
                d['Manufacturer'].append(get_Manufacturer(new_soup))

            
                amazon_df = pd.DataFrame.from_dict(d)
                amazon_df['Product Name'].replace('', np.nan, inplace=True)
                amazon_df = amazon_df.dropna(subset=['Product Name'])
                amazon_df.to_csv("amazon_bags_data.csv", header=True, index=False) 

            else:
                print(link)
                new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                # Function calls to display all necessary product information
                d['Product URL'].append(get_url(new_soup))
                d['Product Name'].append(get_title(new_soup))
                d['Product Price'].append(get_price(new_soup))
                d['Rating'].append(get_rating(new_soup))
                d['Number of Reviews'].append(get_review_count(new_soup))
                d['availability'].append(get_availability(new_soup))
                d['ASIN'].append(get_asin(new_soup))
                d['Product Description'].append(get_productdescription(new_soup))
                d['Manufacturer'].append(get_Manufacturer(new_soup))

            
                amazon_df = pd.DataFrame.from_dict(d)
                amazon_df['Product Name'].replace('', np.nan, inplace=True)
                amazon_df = amazon_df.dropna(subset=['Product Name'])
                amazon_df.to_csv("amazon_bags_data.csv", header=True, index=False)