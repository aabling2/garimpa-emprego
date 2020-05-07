import os
import numpy as np
import glob
import shutil
from flask import flash
from datetime import datetime

# Create a folder by name passed
def Create_folder(folder_name):
    try:
        os.mkdir(folder_name) 
        print('-->Pasta "' + folder_name + '" criada com sucesso!')
    
    except FileExistsError:
        print('-->Pasta "' + folder_name + '" já existe!')

# Save parameters
def Save_data(data, filename):

    try:
        np.save(filename, np.array(data))

        print('Dados salvos em: ' + filename)

    except:
        print('Dados não puderam ser salvos em: ' + filename)

# Load parameters
def Load_data(data, filename):

    try:
        data = np.load(filename+".npy", allow_pickle=True)
    
        print('Dados carregados de: ' + filename)
        
        return data

    except:
        print('Dados não puderam ser carregados de: ' + filename)

        return data

# Get date of all existing files
def Get_files_date(path, extension):

    date_files = []
    date_str = ""

    try:
        dir_files = glob.glob(path+extension)
        for files in dir_files:
            idx_start = len(path)
            idx_end = files.index('_')
            if files[idx_start:idx_end] != date_str:
                date_str = files[idx_start:idx_end]
                date_files.append(date_str)

        return date_files
        
    except:
        print('Não foi possível carregar ou não existem arquivos ainda.')
        return date_files

# Copy files of date selected and update the day
def Update_files_date(paths, sel_date, extension):

    try:
        for folder in paths:
            dir_files = glob.glob(folder+sel_date+extension)
            for files in dir_files:
                print(files)
                today = datetime.now()
                date = str(today.month) + '-' + str(today.day)
                filename = folder + date + files[files.index('_'):]
                if sel_date == date:
                    flash('Arquivos selecionados já estam atualizados para esta data.')
                    return
                else:
                    shutil.copy(files, filename)
        flash('Arquivos atualizados para esta data.')

    except:
        flash('Não foi possível atualizar todos arquivos.')

# Delete files of seleceted date
def Delete_files_date(paths, sel_date, extension):

    try:
        for folder in paths:
            dir_files = glob.glob(folder+sel_date+extension)
            for files in dir_files:
                os.remove(files)

        flash('Arquivos removidos para esta data.')

    except:
        flash('Não foi possível remover os arquivos.')

# Extend list
def List_extension(data_extension):

    list_extension = []

    for items in data_extension:
        list_extension.extend(items)
    
    return list_extension
