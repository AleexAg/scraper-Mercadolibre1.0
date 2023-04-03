from proxy import fetch, fetch_proxies, fetch_proxies_one, fetch_proxies_two, fetch_proxies_three
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import pandas as pd
import datetime

# Main variables
NUM_THREADS = 10
custId = '191222360'   # CHANGE THIS
CategoriesWithSub = []
CategoriesWithOutSub = []
products_data = []


# Get the categories of publications
def getMoreCategory(link):
    try:
        # Conexion to get content
        responseCategory = None
        while responseCategory == None:
            responseCategory = fetch(link)
            if not responseCategory:
                responseCategory = fetch_proxies(link)
                if not responseCategory:
                    responseCategory = fetch_proxies_one(link)
                    if not responseCategory:
                        responseCategory = fetch_proxies_two(link)
                        if not responseCategory:
                            responseCategory = fetch_proxies_three(link)

        # Requests basic config
        CategorySoup = BeautifulSoup(responseCategory.content, 'html.parser')
        CategoriesWithSub.remove(link)

        # Get info
        getLinkByCategory(CategorySoup)
    except:
        print("No more subcategories")


# Get information on the quantity of sales
def getTotalSold(name):
    try:
        # Connection to get information from the seller
        response = None
        while response == None:
            response = fetch(f'https://www.mercadolibre.com.co/perfil/{name}')
            if not response:
                response = fetch_proxies(f'https://www.mercadolibre.com.co/perfil/{name}')
                if not response:
                    response = fetch_proxies_one(f'https://www.mercadolibre.com.co/perfil/{name}')
                    if not response:
                        response = fetch_proxies_two(f'https://www.mercadolibre.com.co/perfil/{name}')
                        if not response:
                            response = fetch_proxies_three(f'https://www.mercadolibre.com.co/perfil/{name}')

        
        # Requests basic config
        SellerProfilesoup = BeautifulSoup(response.content, 'html.parser')
        infoSeller = SellerProfilesoup.find('p', {'class': 'seller-info__subtitle-sales'}).text

        # Add to info
        products_data.append({'seller_info':infoSeller})

    except:
        print("Error on looking info")

# Get link of product by category
def getLinkByCategory(pageSoup:BeautifulSoup):

    # BeautifulSoup configuration
    titleCategory = pageSoup.find('div', {'class': 'ui-search-filter-dt-title'})
    
    title = titleCategory.get_text()
    if title == 'Categorías':

        # Get categories
        listCategories = titleCategory.find_previous('div', {'class': 'ui-search-filter-dl shops__filter-items'})
        categories = listCategories.find_all('li', {'class': 'ui-search-filter-container shops__container-lists'})
        
        if (len(categories) > 9):
            linkMoreCategories = listCategories.find('a', {'class': 'ui-search-modal__link ui-search-modal--default ui-search-link'})['href']  
            try:
                # Conexion to link
                res = None
                while res == None:
                    res = fetch(linkMoreCategories)
                    if res == None:
                        res = fetch_proxies(linkMoreCategories)
                        if res == None:
                            res = fetch_proxies_one(linkMoreCategories)
                            if res == None:
                                res = fetch_proxies_two(linkMoreCategories)
                                if res == None:
                                    res = fetch_proxies_three(linkMoreCategories)
            except:
                print('Error to get Link categories')

            # BeautifulSoup Config
            CategoryPage = BeautifulSoup(res.content, 'html.parser')
            linkCategories = CategoryPage.find('div', {'class': 'ui-search-search-modal-grid-columns'})
            links = linkCategories.find_all('a', {'class': 'ui-search-search-modal-filter ui-search-link'})

            for linkCategory in links:
                try:
                    # Conexion to link
                    res = None
                    while res == None:
                        res = fetch(linkCategory.get('href'))
                        if res == None:
                            res = fetch_proxies(linkCategory.get('href'))
                            if not res:
                                res = fetch_proxies_one(linkCategory.get('href'))
                                if not res:
                                    res = fetch_proxies_two(linkCategory.get('href'))
                                    if not res:
                                        res = fetch_proxies_three(linkCategory.get('href'))

                    # BeautifulSoup config
                    page = BeautifulSoup(res.content, 'html.parser')
                    itemsResult = int(page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '').replace('.', ''))
                    
                    # Add to CategoriesWithSub or CategoriesWithOutSub
                    if itemsResult > 2000:
                        CategoriesWithSub.append(linkCategories.get('href'))
                    else:
                        CategoriesWithOutSub.append(linkCategory.get('href'))

                except:
                    print("Error to search link category")
        else:
            for category in categories:
                linkCategory = category.find('a', {'class': 'ui-search-link'})['href']
                try:
                    res = None
                    while res == None:
                        res = fetch(linkCategory)
                        if not res:
                            res = fetch_proxies(linkCategory)
                            if not res:
                                res = fetch_proxies_one(linkCategory)
                                if not res:
                                    res = fetch_proxies_two(linkCategory)
                                    if not res:
                                        res = fetch_proxies_three(linkCategory)

                    # BeautifulSoup Config
                    page = BeautifulSoup(res.content, 'html.parser')

                    # Get quantity items
                    itemsResult = int(page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '').replace('.', ''))
                    
                    if itemsResult > 2000:
                        CategoriesWithSub.append(linkCategory)
                    else:
                        CategoriesWithOutSub.append(linkCategory)
                except Exception as e:
                    print("Error to search link category 2", e)

    if title == 'Precio':
        listCategories = titleCategory.find_previous('div', {'class': 'ui-search-filter-dl shops__filter-items'})
        categoriesByPrice = listCategories.find_all('li', {'class': 'ui-search-filter-container shops__container-lists'})
        
        for category in categoriesByPrice:
            listPrice = category.find('a', {'class': 'ui-search-link'})['href']
            try:
                # Conexion to listPrice
                res = None
                while res == None:
                    res = fetch(listPrice)
                    if not res:
                        res = fetch_proxies(listPrice)
                        if not res:
                            res = fetch_proxies_one(listPrice)
                            if not res:
                                res = fetch_proxies_two(listPrice)
                                if not res:
                                    res = fetch_proxies_three(listPrice)
                            
                # BeautifulSoup config            
                page = BeautifulSoup(res.content, 'html.parser')
                itemsResult = int(page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '').replace('.', ''))

                if itemsResult > 2000:
                    CategoriesWithSub.append(listPrice)
                else:
                    CategoriesWithOutSub.append(listPrice)
            except:
                print("Error to search link category")

    if len(CategoriesWithSub) > 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            executor.map(getMoreCategory, CategoriesWithSub)


# GET PRODUCT ID
def get_id(url:str) -> str:

    url_list = url.split('/')
    product_id = ''

    if 5 > len(url_list):
        product_id = url_list[3]
        product_id = product_id.split('-')
        product_id = product_id[0] + product_id[1]
    else:
        product_id = url_list[5]
        product_id = product_id.split('?')
        product_id = product_id[0]
    return product_id



# GET INFORMATION
def getInformationOlList(soup: BeautifulSoup):
    try:
        section = soup.find('section', {'class': 'ui-search-results ui-search-results--without-disclaimer shops__search-results'})
        rawItemList = section.find_all('li', {'class': 'ui-search-layout__item'})

        for item in rawItemList:
            try:
                # ADD INFO TO ARRAY
                with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                    executor.submit(
                        products_data.append({
                            'titles': item.find('h2', {'class': 'ui-search-item__title'}).text,
                            'prices': item.find('span', {'class': 'price-tag-fraction'}).text.replace(',', ''),
                            'urls': item.find('a', {'class': 'ui-search-item__group__element'})['href'],
                            'id_product': get_id(item.find('a', {'class': 'ui-search-item__group__element'})['href']),
                            'main_image': item.find('img', {'class': 'ui-search-result-image__element'})["data-src"]
                            })
                        )
            except Exception as r:
                pass

    except Exception as e:
        print("Error get element Ol", e)

# Get information
def getInformation(soup: BeautifulSoup) -> None:
    try:
        # Get all items
        rawItemList = soup.find_all('li', {'class': 'ui-search-layout__item'})

        for item in rawItemList:
            try:
                # Add items to array
                with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                    executor.submit(
                        products_data.append({
                            'titles': item.find('h2', {'class': 'ui-search-item__title'}).text,
                            'prices': item.find('span', {'class': 'price-tag-fraction'}).text.replace(',', ''),
                            'urls': item.find('a', {'class': 'ui-search-item__group__element'})['href'],
                            'id_product': get_id(item.find('a', {'class': 'ui-search-item__group__element'})['href']),
                            'main_image': item.find('img', {'class': 'ui-search-result-image__element'})["data-src"]
                            })
                        )
                
            except Exception as r:
                pass
    except:
        # Get items by list
        getInformationOlList(soup)
        print("Error to get information")

def pagination(nextPage, isNextPage, isFirstPage, soup): 

    if not nextPage:
        return
    if isFirstPage == '1':
        getInformation(soup)

    if nextPage and isNextPage == 'Siguiente':
        try:
            # Conexion with next page
            responseNextPage = None
            while responseNextPage == None:
                responseNextPage = fetch(nextPage)
                if not responseNextPage:
                    responseNextPage = fetch_proxies(nextPage)
                    if not responseNextPage:
                        responseNextPage = fetch_proxies_one(nextPage)
                        if not responseNextPage:
                            responseNextPage = fetch_proxies_two(nextPage)
                            if not responseNextPage:
                                responseNextPage = fetch_proxies_three(nextPage)

            # BeautifulSoup Config
            soupNextPage = BeautifulSoup(responseNextPage.content, 'html.parser')

            getInformation(soupNextPage)
            
            # Get links
            nextPageResult = soupNextPage.find('a', {'class': 'andes-pagination__link', 'title': 'Siguiente'})['href']
            isNextPageResult = soupNextPage.find('a', {'class': 'andes-pagination__link', 'title': 'Siguiente'})['title']
            
            if nextPageResult and isNextPageResult:
                pagination(nextPageResult, isNextPageResult, '0', soupNextPage)

        except:
            print("end code")

def searchItems(link):
    try:
        # Conexion to search items
        responseCategory = None
        while responseCategory == None:
            responseCategory = fetch(link)
            if not responseCategory:
                responseCategory = fetch_proxies(link)
                if not responseCategory:
                    responseCategory = fetch_proxies_one(link)
                    if not responseCategory:
                        responseCategory = fetch_proxies_two(link)
                        if not responseCategory:
                            responseCategory = fetch_proxies_three(link)

        # BeautifulSoup config
        CategorySoup = BeautifulSoup(responseCategory.content, 'html.parser')

        try:
            nextPage = CategorySoup.find('a', {'class': 'andes-pagination__link'})['href']
            isNextPage = CategorySoup.find('a', {'class': 'andes-pagination__link'})['title']
            isFirstPage = CategorySoup.find('span', {'class':'andes-pagination__link'}).text

            if nextPage and isNextPage:
                pagination(nextPage, isNextPage, isFirstPage, CategorySoup)
        except:
            getInformation(CategorySoup)
            
    except:
        print("Error to get items")


# Get information with products
def get_info(product):
    try:
        # Conexion product
        res = None
        while res == None:
            res = fetch(product['urls'])
            if not res:
                res = fetch_proxies(product['urls'])
                if not res:
                    res = fetch_proxies_one(product['urls'])
                    if not res:
                        res = fetch_proxies_two(product['urls'])
                        if not res:
                            res = fetch_proxies_three(product['urls'])

        # Config
        ItemSoup = BeautifulSoup(res.content, 'html.parser')
        ItemSoup2 = BeautifulSoup(res.text, 'html.parser')

        try:
            # Sold items
            countSold = ItemSoup.find('span', {'class': 'ui-pdp-subtitle'}).text
            product['sold'] = countSold[10:]
        except:
            pass
        
        try:
            # Get description
            itemsInfo = ItemSoup2.findAll('div', {'class': 'ui-pdp-container__row--description'})
            for ele in itemsInfo:
                description = ele.find('p')
                dedsc = description.get_text()

                product['description'] = dedsc

        except Exception as descError2:
            pass
        
        try:
            # Get second and third images
            imagesContent = ItemSoup.find_all('div', {'class': 'ui-pdp-thumbnail__picture'})
            
            for item in imagesContent:
                images = item.find('img', {'class': 'ui-pdp-image'})
                desc = ''
                for num in images['alt']:
                    images = item.find('img', {'class': 'ui-pdp-image'})
                    desc += num

                    first = images['data-src']
                    if desc == 'Imagen 1':
                        pass
                    if desc == 'Imagen 2':
                        product['second_image'] = first
                    if desc == 'Imagen 3':
                        product['third_image'] = first
        except:
            pass
                
    except Exception as e:
        pass


def main():
    # Start time
    y = datetime.datetime.now()
    print(y)

    print("Start scraping... please wait...")
    try:
        # First conexion ONLY listado.mercadolibre.com.co
        response = fetch_proxies('https://listado.mercadolibre.com.co/_CustId_'+custId+'_PrCategId_AD')

        # BeautifulSoup Config
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get seler name
        name_seler = soup.find('h1', {'class': 'ui-search-breadcrumb__title'}).text[17::].replace(' ', '+')

        getLinkByCategory(soup)
        getTotalSold(name_seler)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                executor.map(searchItems, CategoriesWithOutSub)
        products_data.sort(reverse=True, key=lambda x:(len(x), repr(x)))
        
        # Delete duplicate products
        for i in range(0, len(products_data)):
            try:
                if products_data[i+1]['id_product'] == products_data[i]['id_product']:
                        products_data.remove(products_data[i])
            except:
                continue

        if len(products_data) % 5000 == 0:
            time_queries = int(len(products_data) / 5000)
        else:
            time_queries = int((len(products_data) // 5000) + 1)
        
        for i in range(0, time_queries):
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                    executor.map(get_info, products_data[0:4999])
        

        # ADD TO EXCEL AND CSV
        frame = pd.DataFrame(products_data)
        frame.to_excel(f'{name_seler}.xlsx', index=False)

    except Exception as E:
        print(E)

    # Print end time
    x = datetime.datetime.now()
    print(x)

if __name__ == '__main__':
    main()