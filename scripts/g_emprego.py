# Modules
import os
import requests
import re
import glob
from bs4 import BeautifulSoup
from datetime import date, datetime
from flask import flash
from googlesearch import search

# Read saved files with url links and pass to a bag of words
def Load_bag_links(keys_init, keys):
    
    bag_links = {}

    for i in keys_init:
        today = datetime.now()
        date = str(today.month) + '-' + str(today.day) + '_'
        file_name = 'links/' + date + keys + '-' + i + '.txt'

        if os.path.isfile(file_name) == True:
            register_links = open(file_name,'r')
            txt_links = register_links.read()
            register_links.close()

            bag_converted = eval(txt_links)
            bag_links.update(bag_converted)

            print("\nArquivo de links: " + file_name)     

        else:
            print("\nArquivo não existe: " + file_name)   

    return bag_links

# Load the backup of results
def Load_bag_results():
    
    bag_links_result = {}

    today = datetime.now()
    date = str(today.month) + '-' + str(today.day) + '_'
    file_name = 'outputs/' + date + (os.path.basename(os.getcwd())) + '.txt'
    
    try:
        if os.path.isfile(file_name) == True:
            register_links_result = open(file_name,'r')
            txt_links = register_links_result.read()
            bag_converted = eval(txt_links)
            bag_links_result.update(bag_converted)
            register_links_result.close()
    except:
        register_links_result = open(file_name,'w')
        register_links_result.close()
        
    return bag_links_result

# Save a backup of results
def Save_bag_results(bag_links_result):

    today = datetime.now()
    date = str(today.month) + '-' + str(today.day)
    file_name = 'outputs/' + date + '_Links.txt'
    
    try:
        with open(file_name, 'w') as f:
            for item in bag_links_result:
                f.write("%s\n" % item)
            f.close
        print("Resultados gravados.")
    except:
        print("Resultados não puderam ser gravados.")
        
# Request content of the url
def Request_content(url):
    soup_url = {}
    try:
        request = requests.get(url, allow_redirects=True, auth=('user', 'pass'), timeout=10)            
        if request.status_code == 200:
            print('A página é válida.')
            soup_url = BeautifulSoup(request.content, 'lxml')
            r_bool_url = True
        else:
            print('A página NÃO é válida.')
            r_bool_url = False
    except:
        print('A página NÃO é válida.')
        r_bool_url = False
        
    return soup_url, r_bool_url

# Configure input parameters in dictionaries
def Set_params_init(init, words, lvs):

    # Keywords to search
    keys_lv = {}
    keys_init = {}

    # Dictionary of keywords / use uppercase at first character / maximum 2 words
    keys_lv1 = {}.fromkeys(words[0],lvs[0])
    keys_lv2 = {}.fromkeys(words[1],lvs[1])
    keys_lv3 = {}.fromkeys(words[2],lvs[2])

    # Dictionary of auxiliary keywords to find jobs / join the main key
    keys_init_lv1 = {}.fromkeys(init,lvs[3])

    # Add configuration to complete dictionaries
    keys_lv.update(keys_lv1)
    keys_lv.update(keys_lv2)
    keys_lv.update(keys_lv3)
    keys_init.update(keys_init_lv1)
    
    print("Palavras chave e pesos aplicados.")

    return(keys_lv, keys_init)

# Research with key words and save all urls
def Research_links(words, keys_init, num_search, keys_all):
    
    os.system('cls')     

    # *Set keys_lv for all keywords or just main level to the search
    if keys_all:
        keys_lv = set(words[0]+words[1]+words[2])
    else:
        keys_lv = words[0]
    print('Entradas de busca:', keys_init)
    print('Palavras de busca:', keys_lv)

    # Estimate time to wait between requests
    time_delay = len(keys_init)*len(keys_lv)*2

    # Do the research by each key word
    for keys in keys_lv:
        try:
            # Join each initial key to key words
            for init in keys_init:    
                
                # Generate the name of the file to save urls
                bag_links = {}
                today = datetime.now()
                date = str(today.month) + '-' + str(today.day) + '_'
                file_name = 'links/' + date + keys + '-' + init + '.txt'

                # Check if file already exist
                if os.path.isfile(file_name):
                    print('Arquivo de links já existe: ' + file_name)

                # Do the research and save to txt file
                else:
                    print(init + ' ' + keys)
                    query = init + ' ' + keys

                    # Get all urls of research
                    # *Pause with long time delay will mantain the connection and not block when have lot of queries 
                    for link_finded in search(query, tld="com", lang='pt', num=num_search, stop=num_search, pause=time_delay):    
                        bag_links[link_finded] = 0

                    # Save each group of urls in txt file
                    txt_data = str(bag_links)
                    register_links = open(file_name,'w')
                    register_links.write(txt_data)
                    register_links.close()
                    print("Arquivo salvo: " + file_name)

                    # End process when detect a stop file
                    if os.path.isfile('stop'):
                        os.remove('stop')
                        return
                    
        # End process when detect error
        # *Normally when has too many requests
        except Exception as e:
            print(e)
            print('Tente novamente mais tarde.')
            break
            
    print("Pesquisa finalizada!")    

# Scrap all urls with key words and count words finded
def Scrap_links(keys_lv, keys_init, lvs):
    
    # Code of webscrapring the links and apply weights
    bag_links_result = {}
    r_bool = True
    keys_lv_init = {}
    keys_lv_init.update(keys_lv)
    keys_lv_init.update(keys_init)
    progress = 0

    # Special condition when search double '+' 
    if 'C++' in keys_lv_init:
        keys_lv_init['C+'] = keys_lv_init.pop('C++')
        
    # Include lower case keys
    lower_keys_lv_init = {}
    for k, v in keys_lv_init.items():
        lower_keys_lv_init[k.lower()] = v
    keys_lv_init.update(lower_keys_lv_init)
                
    # Read data from txt to load links already processed to bag_links_result
    bag_links_result = Load_bag_results()

    # Set keys_lv for all keywords or just one level
    for keys_file in keys_lv:

        bag_links = {}
        bag_links = Load_bag_links(keys_init, keys_file)
        
        # Delete links in bag_links that already exists on results
        for i in bag_links_result:
            if i in bag_links:
                print("URL já processada: ", i)
                del bag_links[i]
        
        # Create a list with index to calculate status process
        bag_links_index = list(bag_links)

        #bag_links_response = bag_links_result.copy().keys()

        # Scrap each url in 
        for url in bag_links:

            #if url not in bag_links_response:

            # Set new values of lvs to zero
            num_lvs = [0, 0, 0, 0]

            # When the url is a pdf don't scrap
            if url.split('.')[-1] == 'pdf':
                continue

            # Show status of process
            os.system('cls') 
            screen = keys_file + '-- Qtd. links: ' + str(len(bag_links))
            screen += str(' --> %.2f'%progress) + '%' + '\n' + url     
            print(screen)          

            # Request pages and get the soup of it
            soup, r_bool = Request_content(url)
            
            # Scrap key words in soup
            for searched_word in keys_lv_init:

                if r_bool is False:
                    break

                results = soup.find_all(string=re.compile(searched_word))
                
                words = None
                searched_word_split = None
                searched_word_split = searched_word.split()

                for text in results:
                    words = text.split()

                    for index, word in enumerate(words):
                        for split_word in searched_word_split:
                            if split_word in word:
                                word = split_word

                        word_double = None
                        if index != 0:
                            word_double = words[index-1]+' '+word

                        # Add counting of searched words
                        if word==searched_word or word_double==searched_word:  
                            value_finded = float(keys_lv_init[searched_word])
                            if value_finded == lvs[0]:
                                num_lvs[0] += 1
                            elif value_finded == lvs[1]:
                                num_lvs[1] += 1
                            elif value_finded == lvs[2]:
                                num_lvs[2] += 1
                            elif value_finded == lvs[3]:
                                num_lvs[3] += 1

                            print('Palavra encontrada: ' + searched_word)

                            break
                    else:
                        continue

                    break

                # Update status of processing
                progress = ((1+bag_links_index.index(url))/len(bag_links_index))*100

                # Update bag links with number of words finded
                bag_links_result[url] = num_lvs

                # Save backup of results each link processed
                today = datetime.now()
                date = str(today.month) + '-' + str(today.day) + '_'
                file_name = 'outputs/' + date + (os.path.basename(os.getcwd())) + '.txt'
                register_links_result = open(file_name,'w')
                txt_data = str(bag_links_result)
                register_links_result.write(txt_data)
                register_links_result.close()
                print("Backup salvo!")

                # End process when detect a stop file
                if os.path.isfile('stop'):
                    os.remove('stop')
                    return

        print('Varredura completa para: '+ keys_file) 

# Calculate and rank list of results 
def Organize_links(keys_init, lvs):

    # Remove non relevant links
    # *Maintain only urls with key words in it
    bag_links_result = Load_bag_results()
    bag_links_result_copy = {}
    bag_links_result_copy.update(bag_links_result)
    for url in bag_links_result_copy:
        repeted = 0
        for link in bag_links_result:
            if link == url:
                repeted += 1
                print(repeted)

    """# Remove repeted urls
    for url in bag_links_result_copy:
        for key in keys_init:        
            if key in url or key.lower() in url:
                rel = True
                break
            else:
                rel = False
                
        if rel == False:
            del bag_links_result[url]
            print('Removed '+ url)"""

    # Save refined links
    Save_bag_results(bag_links_result)
        
    # Calculate weights
    for url in bag_links_result:
        values = bag_links_result[url]
        calc_result = [lvs[0]*values[0], lvs[1]*values[1], lvs[2]*values[2], lvs[3]*values[3]]
        calc_result = sum(calc_result)
        bag_links_result[url] = calc_result

    # Organize list by weights
    bag_links_rank = []
    bag_links_rank = sorted(bag_links_result.items(), key=lambda x: x[1], reverse=True)

    
    """for i, bags in bag_links_sorted:
        bag_links_rank = [idx for idx, val in bag_links_sorted]"""

    flash('Total de links: ' + str(len(bag_links_rank)))

    # Save list if it's not empty
    if bag_links_rank:
        Save_bag_results(bag_links_rank)
        flash("Lista de resultados completo!")
    else:
        flash("Sem resultados!")

# Get all files in path
# *Used to get urls from results
def Get_files_path(path, extension):

    output_files = []
    result_links = []
    try:
        dir_output_files = glob.glob(path+extension)
        
        for files in dir_output_files:
            output_files.append(files[len(path):])
            f = open(files, "r")
            result_links.append(f.read().split())
            f.close()
            print('Arquivo carregado: ' + str(files))

        return result_links, output_files
        
    except:
        print('Não foi possível ou não existem arquivos para carregar.')
        return result_links, output_files
