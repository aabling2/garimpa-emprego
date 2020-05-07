import os
import argparse
from scripts import cv_reader as CVreader
from scripts import g_emprego as Gemprego
from scripts import others as OT
from scripts import dictionary as DICT
from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.utils import secure_filename

# Create app with Flask
app = Flask(__name__)
app.secret_key = os.urandom(42)

# Definitions
FOLDER_LINKS = 'links/'
FOLDER_OUTPUTS = 'outputs/'
FOLDER_INTERN = 'static/'
keys_lv, keys_init,  = {}, {}
scan_words, result_links, output_files, date_files, dict_words = [], [], [], [], []
num_search, num_results, sel_list, process_check = 100, 200, 0, 0
href_link, filename, sel_date = "", "", ""
init = ['Vaga', 'Emprego']
words = [['Visao Computacional', 'Computer Vision','Engenharia Eletrica'], 
        ['Inteligencia Artificial', 'Mecatronica', 'Automação'],
        ['Projetista', 'Desenvolvedor']]
lvs = ["7.0", "3.0", "2.5", "5"]

# Route of main page
@app.route('/', methods = ['GET','POST'])
# Do the comunication/logic between requests and functions
def main():

    # Set global variables
    global keys_lv, keys_init, scan_words, result_links, output_files, date_files, dict_words
    global num_search, num_results, sel_list, process_check, keys_all, href_link, filename, sel_date
    global init, words, lvs

    # Set lists with variables to save in numpy file
    data_update1 = [filename, init, words, num_search, num_results, lvs]
    data_update2 = []
    keys_all = False

    # Receive GET from page request
    if request.method == 'GET':
        date_files = OT.Get_files_date(FOLDER_LINKS, '*.txt')

    # Receive POST from page request
    if request.method == 'POST':

        # Items to update from page
        if 'number_search' in request.form: num_search = int(request.form['number_search'])
        if 'number_results' in request.form: num_results = int(request.form['number_results'])
        if 'weight1' in request.form: lvs[0] = float(request.form['weight1'])
        if 'weight2' in request.form: lvs[1] = float(request.form['weight2'])
        if 'weight3' in request.form: lvs[2] = float(request.form['weight3'])
        if 'weight4' in request.form: lvs[3] = float(request.form['weight4'])
        if 'search_all' in request.form: keys_all = True

        # Open a pdf file, save in static
        if 'open' in request.form:
            if request.files.get('file'):
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.save(FOLDER_INTERN+filename)    
                flash('Arquivo carregado.')
            else:
                flash('O arquivo não foi selecionado!')         

        # Scan pdf, read text and delete pdf file
        elif 'scan' in request.form:
            if filename:
                pdf_file = FOLDER_INTERN+filename
                CVreader.Convert_PDF2Txt(pdf_file, FOLDER_OUTPUTS)
                dict_words = OT.Load_data(DICT.bad_words, 'dict')
                scan_words = CVreader.Filter_words(DICT.bad_chars, DICT.bad_content, dict_words)
                dict_compare = OT.List_extension([init, words[0], words[1], words[2]])
                scan_words = CVreader.Compare_lists_remove(dict_compare, scan_words)
                flash('Leitura do documento finalizada e palavras coletadas.')
            else:
                flash('Arquivo não selecionado!')     

        # Research with key words and save all urls
        elif 'search' in request.form:
            OT.Save_data(data_update1, 'presets')
            keys_lv, keys_init = Gemprego.Set_params_init(init, words, lvs)
            Gemprego.Research_links(words, keys_init, num_search, keys_all)
            flash('Pesquisa finalizada!')
            process_check = 1

        # Scrap all urls with key words and count words finded
        elif 'scrap' in request.form:
            if process_check == 1:
                OT.Save_data(data_update1, 'presets')
                keys_lv, keys_init = Gemprego.Set_params_init(init, words, lvs)
                Gemprego.Scrap_links(keys_lv, keys_init, lvs)
                flash('Scrapping finalizado!')
                process_check = 2
            else:
                flash('Requer processo anterior.')

        # Apply math to each link result and rank list
        elif 'list_results' in request.form:
            OT.Save_data(data_update1, 'presets')
            Gemprego.Organize_links(keys_init, words, num_results, lvs, FOLDER_OUTPUTS)
            result_links, output_files = Gemprego.Get_files_path(FOLDER_OUTPUTS, '*_Links.txt')
            data_update2 = list(OT.Load_data(data_update2, 'urls'))
            process_check = 0
            if result_links or output_files:
                return render_template('links.html', result_links=result_links, output_files=output_files
                                                    , sel_list=sel_list, href_link=href_link, data_links=data_update2)
        
        # Open the page with results and saved links
        elif 'manage' in request.form:
            result_links, output_files = Gemprego.Get_files_path(FOLDER_OUTPUTS, '*_Links.txt')
            data_update2 = list(OT.Load_data(data_update2, 'urls'))
            if result_links or output_files:
                return render_template('links.html', result_links=result_links, output_files=output_files
                                                    , sel_list=sel_list, href_link=href_link, data_links=data_update2)
            else:
                flash('Nada a mostrar!')

        # Save url opened to saved links
        elif 'save_link' in request.form:
            data_update2 = list(OT.Load_data(data_update2, 'urls'))
            if href_link in data_update2:
                flash('URL já existe no banco de dados.')
            elif href_link != "":
                data_update2.append(href_link)
                OT.Save_data(data_update2, 'urls')
                flash('URL salva.')
            return render_template('links.html', result_links=result_links, output_files=output_files
                                                , sel_list=sel_list, href_link=href_link, data_links=data_update2)

        # Delete url from saved links
        elif 'del_link' in request.form:
            data_update2 = list(OT.Load_data(data_update2, 'urls'))
            b_link = False
            if href_link in data_update2:
                b_link = True
            if b_link is True:
                data_update2.remove(href_link)
                flash('URL deletada:'+ href_link)
                OT.Save_data(data_update2, 'urls')
            return render_template('links.html', result_links=result_links, output_files=output_files
                                                , sel_list=sel_list, href_link=href_link, data_links=data_update2)

        # Copy files with date selected and update their date to the current day
        elif 'update_files' in request.form:
            OT.Update_files_date([FOLDER_LINKS,FOLDER_OUTPUTS], sel_date, '*.txt')
            date_files = OT.Get_files_date(FOLDER_LINKS, '*txt')

        # Delete files with the date selected
        elif 'clear_files' in request.form:
            OT.Delete_files_date([FOLDER_LINKS,FOLDER_OUTPUTS], sel_date, '*.txt')
            date_files = OT.Get_files_date(FOLDER_LINKS, '*txt')
            process_check = 0
        
        # Back from results page to main page
        elif 'back_page' in request.form:
           filename, init, words, num_search, num_results, lvs = OT.Load_data(data_update1, 'presets')

        # Stop running with research or scrapping
        elif 'stop' in request.form:
            with open('stop', 'w') as stop_file:
                stop_file.close()
            flash('Atividade interrompida.')

        elif 'set_params' in request.form:
            flash('Parâmetros salvos.')

    # Update page with new values
    return render_template('index.html',
        filename=filename,
        keys_init=init,
        keys_lv1=words[0],
        keys_lv2=words[1],
        keys_lv3=words[2],
        num_search=str(num_search),
        num_results=str(num_results),
        lv1=lvs[0],
        lv2=lvs[1],
        lv3=lvs[2],
        lv4=lvs[3],
        scan_words=scan_words,
        date_files=date_files,
        keys_all=keys_all)

# Route to get ajax post of data to update from main page
@app.route('/update1', methods = ['POST'])
def update1():

    # Set global variables
    global keys_lv, keys_init, scan_words, result_links, output_files, date_files, dict_words
    global num_search, num_results, sel_list, href_link, filename, sel_date
    global init, words, lvs
    
    # Receive POST from page request
    if request.method == 'POST':

        # Get ajax data request
        data_update = request.json

        # Variables to update
        init = data_update[0]
        words[0] = data_update[1]
        words[1] = data_update[2]
        words[2] = data_update[3]
        sel_date = data_update[4]
        del_word = data_update[5]

        # Set lists to compare and append or remove items
        dict_compare = OT.List_extension([init, words[0], words[1], words[2]])
        dict_words = list(OT.Load_data(DICT.bad_words, 'dict'))
        dict_words = list(dict.fromkeys(dict_words))
        scan_words = list(dict.fromkeys(scan_words))

        # Remove add words received in dict_compare
        dict_compare_low = [x.lower() for x in dict_compare]
        dict_words = CVreader.Compare_lists_remove(dict_compare_low, dict_words)
        scan_words = CVreader.Compare_lists_remove(dict_compare, scan_words)

        # Include words to dictionary of bad words
        if del_word:
            if del_word.lower() not in dict_words:
                dict_words.append(del_word.lower())
                scan_words.remove(del_word)
                print("Item excluído:", del_word.lower())

        # Save changes to dictionary of bad words and set parameters
        OT.Save_data(dict_words, 'dict')
        keys_lv, keys_init = Gemprego.Set_params_init(init, words, lvs)

    # Redirect to main page
    return redirect('/')

# Route to get ajax post of data to update from results page
@app.route('/update2', methods = ['POST'])
def update2():

    # Set global variables
    global sel_list, href_link, output_files, result_links
    
    # Receive POST from page request
    if request.method == 'POST':
        data_update = request.json

        sel_list = data_update[0]
        href_link = data_update[1]

    # Update page with new values
    return render_template('links.html', 
        result_links=result_links, 
        output_files=output_files, 
        sel_list=sel_list, 
        href_link=href_link)

# Main execution
if __name__ == '__main__':
    
    # Create necessary folders
    OT.Create_folder('outputs')
    OT.Create_folder('links')

    # Receive arguments to set local port
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default='5000' , help = 'Numeração da porta para gerar servidor')
    args = parser.parse_args()

    # Run Flask application
    app.run(debug=True, host='0.0.0.0', threaded=True, port=args.port)