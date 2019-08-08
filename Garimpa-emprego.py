# Modules
import os
import os.path
import requests
import re
import webbrowser
from googlesearch import search 
from bs4 import BeautifulSoup
from datetime import date
from IPython.display import clear_output

#---------------------------------------

# Function to create folders
def Create_folder(folder_name):
    
    try:
        os.mkdir(folder_name) 
        print('Pasta "', folder_name, '" criada com sucesso!')
    
    except FileExistsError:
        print('Pasta "', folder_name, '" já existe!')


# Function to read saved files with url links and pass to a bag of words
def Load_bag_links(keys):

    file_exist = False
    file_name = 'Links/' + keys + '.txt'
    
    if os.path.isfile(file_name) == True:
        register_links = open(file_name,'r')
        file_exist = True
        txt_links = register_links.read()
        register_links.close()
        
        bag_converted = eval(txt_links)
        bag_links.update(bag_converted)
        
        print("\nArquivo de links: ", file_name)     
        
    else:
        file_exist = False
        print("\nArquivo não existe: ", file_name)   
    
    return bag_links

# Function to load the backup of results
def Load_bag_results():
    
    file_name = 'Backups/' + (os.path.basename(os.getcwd())) + '-results-backup.txt'
    
    try:
        register_links_result = open(file_name,'r')
        txt_links = register_links_result.read()
        bag_converted = eval(txt_links)
        bag_links_result.update(bag_converted)
        register_links_result.close()
    except:
        register_links_result = open(file_name,'w')
        register_links_result.close()
        
    return bag_links_result

# Function to request content of the url
def Request_content(url):
    try:
        request = requests.get(url, allow_redirects=True, auth=('user', 'pass'), timeout=10)            
        if request.status_code == 200:
            print('A página é válida')
            soup = BeautifulSoup(request.content, 'lxml')
            r_bool = True
        else:
            print('A página NÃO é válida')
            r_bool = False
    except:
        print('A página NÃO é válida')
        r_bool = False
        
    return soup, r_bool

print('Funções OK')

#---------------------------------------

# Code to init inputs of the searching
# Bag of links
bag_links = {}

# Keywords to search
keys_lv = {}

# Level 1 highest priority to search loops / weights / don't put too much key, provide error of requests
lv1 = 5.0
lv2 = 3.0
lv3 = 2.5
lv4 = 2.0

# Dictionary of keywords / use uppercase at first character / maximum 2 words
keys_lv1 = {}.fromkeys(['Visao Computacional'],lv1)
keys_lv2 = {}.fromkeys(['Inteligencia Artificial', 'GPU', 'CUDA', 'Qt Creator', 'OpenCV', 'Unreal Engine', 'Unity', 'Projetos', 
                        'C++', 'Python', 'Programador', 'Engenharia Eletrica', 'Mecatronica', 'Automação', 'Robotica'],lv2)
keys_lv3 = {}.fromkeys(['Projetista', 'Desenvolvedor', 'Desenhista', 'Cadista', 'Cad', 'Autocad'],lv3)

# Dictionary of auxiliary keywords to find jobs / join the main key
keys_init = {}.fromkeys(['Vaga', 'Emprego', 'Oportunidade', 'Startup', 'Junior', 'Pleno', 'Auxiliar', 'Tecnico', 'Assistente', 'Analista', 'Trainee', 'Engenheiro'],lv4)

keys_lv.update(keys_lv1)
keys_lv.update(keys_lv2)
keys_lv.update(keys_lv3)

print(keys_lv)
print(keys_init)

#---------------------------------------

# Code to research and save links
# Number of searches for each subject
num_search = 100

Create_folder('Links')

# Set keys_lv for all keywords or just one level
for keys in keys_lv1:
    try:
        bag_links = {}
        file_exist = False
        time_delay = len(keys_lv)+len(keys_init)
        file_name = 'Links/' + keys + '.txt'

        if os.path.isfile(file_name) == True:
            file_exist = True
        else:
            file_exist = False
            register_links = open(file_name,'w')

        for init in keys_init:    
            if file_exist == True:
                print('Arquivo de links já existe: ' + file_name)
                register_links.close()   
                break
            
            print("\033[1m" + init + ' ' + keys + "\033[0;0m")
            query = init + ' ' + keys
            
            # Pause with long time delay will mantain the connection and not block when have lot of queries 
            for link_finded in search(query, tld="co.in", lang='pt', num=num_search, stop=num_search, pause=time_delay*1.5):    
                bag_links[link_finded] = 0

        if file_exist == False:
            txt_data = str(bag_links)
            register_links.write(txt_data)
            register_links.close()
            print("Arquivo salvo: ", file_name)
            
    except:
        if file_exist == False:
            register_links.close()
            os.remove(file_name)
            print("Erro na requisição de páginas")
            print("Arquivo removido: ", file_name)
            break
        
print("Pesquisa finalizada!")

#---------------------------------------

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
    
Create_folder('Backups')
    
# Read data from txt to load links already processed to bag_links_result
bag_links_results = Load_bag_results()

# Set keys_lv for all keywords or just one level
for keys in keys_lv1:

    bag_links = {}
    bag_links = Load_bag_links(keys)
    
    # Delete links in bag_links that already exists on results
    for i in bag_links_result:
        if i in bag_links:
            del bag_links[i]
    
    bag_links_index = []
    for index_link, link in enumerate(bag_links):
        bag_links_index.append(link)
    
    for url in bag_links:
        
        if url.split('.')[-1] == 'pdf':
            continue
            
        clear_output(wait=True)
        file_name = 'Links/' + keys + '.txt'
        print("\nArquivo de links: ", file_name, ' -- Qtd. links: ', len(bag_links))   
        print('--> %.2f'%progress, '%')
        print('\n\033[1m'+url+'\033[0;0m')

        soup, r_bool = Request_content(url)
        
        for searched_word in keys_lv_init:

            if r_bool is False:
                break

            keys_lv_init[searched_word.lower()] = keys_lv_init.value()            

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

                    if word==searched_word or word_double==searched_word:         
                        bag_links[url] += keys_lv_init[searched_word_original]
                        print('Palavra encontrada: ', searched_word)

                        break
                else:
                    continue

                break

        # Update status of processing
        progress = ((1+bag_links_index.index(url))/len(bag_links_index))*100
        
        # Update results
        bag_links_result[url] = bag_links[url]

        # Save backup of results each link processed
        file_name = 'Backups/' + (os.path.basename(os.getcwd())) + '-results-backup.txt'
        register_links_result = open(file_name,'w')
        txt_data = str(bag_links_result)
        register_links_result.write(txt_data)
        register_links_result.close()
        print("Backup salvo!")

    print('\nVarredura completa para: ', keys)

print('\nVarredura de páginas completa!')

#---------------------------------------

# Code to organize by the weights
bag_links_sorted = sorted(bag_links_result.items(), key=lambda x: x[1], reverse=True)

for i, bags in bag_links_sorted:
    bag_links_rank = [idx for idx, val in bag_links_sorted]

print('\033[1mTotal de links: ', len(bag_links_rank), '\033[0;0m')

#---------------------------------------

# Code to limit rank and create a HTML archive with the results
limit_rank = 1000
html_links = ""
html_keys1 = ""
html_keys2 = ""
html_keys3 = ""

file_name_html = 'G_Emprego-Resultados.html'
f = open(file_name_html,'w')   

for search_word in keys_lv1.keys():
    html_keys1 += ' ' + search_word + ' /'

for search_word in keys_lv2.keys():
    html_keys2 += ' ' + search_word + ' /'
    
for search_word in keys_lv3.keys():
    html_keys3 += ' ' + search_word + ' /'

count = 1
for url in bag_links_rank:
    html_links += '<p>' + str(bag_links_rank.index(url)+1) + '- <a href=' + url + '>' + url + '</a></p>'
    count+=1
    if count > limit_rank:
        break
        
html_code = '<html>' + '<p>Prioridade 1 -->' + html_keys1 + '</p><p>Prioridade 2 -->' + html_keys2 + '</p><p>Prioridade 3 -->' + html_keys3 + '</p>' + html_links + '</html>'

f.write(html_code)

webbrowser.open(file_name_html)

f.close()
