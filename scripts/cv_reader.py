# Modules
import sys 
import os
import unicodedata
import glob
import PyPDF2

# Read pdf file and extract text 
def Convert_PDF2Txt(PDF_file, save_path):

    pdfFileObject = open(PDF_file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        text += page.extractText()

    pdfFileObject.close()

    # Save text extracted
    with open(save_path+'pdf_text.txt', 'w') as f:
        f.write(text)
        f.close

    # Remove pdf files not in usage
    dir_pdf_files = glob.glob("static/*.pdf")
    for files in dir_pdf_files:
        if files[7:] != PDF_file[7:]:
            os.remove(files)

    print('Leitura do documento finalizada.')

# Apply filter to text extracted with database words
def Filter_words(bad_chars, bad_content, bad_words):
    
    # Read text file
    filetxt = "outputs/pdf_text.txt"
    f = open(filetxt, "r") 
    content = f.read()
    f.close()

    # Remove special characters and numbers
    content = str(unicodedata.normalize('NFKD', content).encode('ASCII','ignore'))
    for i in bad_chars : 
        content = content.replace(i, '')
    content = list(content.split())

    # Remove words that don't are good for key words
    scan_words = []
    for key in content:
        key_low = key.lower()
        if key_low not in bad_words:
            b_el = False
            for el in bad_content:
                if el in key_low: 
                    b_el = True
                    break
            if b_el is False:
                scan_words.append(key_low.capitalize())

    scan_words = list(dict.fromkeys(scan_words))

    print("Palavras coletadas.")

    return scan_words

# Compare if items in one list are in another and remove them 
def Compare_lists_remove(static_list, change_list):

    for items in static_list:
        if items in change_list:
            change_list.remove(items)

    return change_list

# Compare if items in one list are in another and add them 
def Compare_lists_append(static_list, change_list):

    for items in static_list:
        if items not in change_list:
            change_list.append(items)

    return change_list