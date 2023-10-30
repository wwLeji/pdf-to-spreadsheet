#!/usr/bin/env python3

import PyPDF2
import re
import pandas as pd
from openpyxl import load_workbook
import os
import shutil
import sys

if len(sys.argv) != 3:
    exit(0)
elif len(sys.argv) == 3:
    start_index = sys.argv[1] + " " + sys.argv[2]

# nom du fichier excel
excel_file_name = "output.xlsx"
# ajouter un espace après l'article ou l'annexe de début
start_index = start_index + " "



def roman_to_int(roman):
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    prev_value = 0
    for numeral in reversed(roman):
        value = roman_numerals[numeral]
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    return result

def int_to_roman(n):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4, 1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syms[i]
            n -= val[i]
        i += 1
    return roman_num

def increment_roman(roman):
    int_value = roman_to_int(roman)
    int_value += 1
    return int_to_roman(int_value)

def guess_end_index(start_index):
    if start_index == "Article 123 ":
        end_index = "Done at Strasbourg, 5 April 2017."
        return end_index
    # Si l'article ou l'annexe de début commence par "Article" ou "ANNEX", on devine l'index de fin
    if start_index.startswith("Article"):
        # On récupère le numéro de l'article ou de l'annexe de début
        start_index_number = re.findall(r'\d+', start_index)[0]
        # On récupère le numéro de l'article ou de l'annexe de fin
        end_index_number = int(start_index_number) + 1
        # On devine l'index de fin
        end_index = start_index.replace(start_index_number, str(end_index_number))
    elif start_index.startswith("ANNEX"):
        # Les numéros d'annexe sont des chiffres romains, incrémentez-les de 1
        annex_number = start_index.split(" ")[1]
        incremented_annex_number = increment_roman(annex_number)
        end_index = f"ANNEX {incremented_annex_number}"
    else:
        # Sinon, on demande à l'utilisateur de saisir l'article ou l'annexe de fin
        end_index = input("Veuillez saisir l'article ou l'annexe de fin : ")
        # Ajouter un espace après l'article ou l'annexe de fin
        end_index = end_index + " "
    return end_index

# appel la fonction guess_end_index et ajouter un espace après l'article ou l'annexe de fin
end_index = guess_end_index(start_index)


# Ouvre le fichier PDF en mode lecture binaire (rb)


# save in output.txt the text between the first "Article 10 " and the first "Article 11 "
with open('text.txt', 'r') as f:
    text = f.readlines()
    for i in range(len(text)):
        # si l'article ou l'annexe de début est trouvé dans la ligne i et que c'est le seul mot de la ligne
        if start_index in text[i] and len(text[i]) == len(start_index) + 1:
            for j in range(i, len(text)):
                if end_index in text[j]:
                    with open('output.txt', 'w') as f:
                        f.write('')
                        f.close()
                    with open('output.txt', 'a') as f:
                        for k in range(i, j):
                            f.write(text[k])
                            # remove all '\n' between the lines
                            if '\n' in text[k+1]:
                                text[k+1] = text[k+1].replace('\n', '')
                            # write '\n' only if the next line start with a number and a dot
                            if re.search(r"^\(([0-9]+)\)|^([0-9]+)\.", text[k+1].strip()):
                                f.write('\n')
                            # write '\n' only if the next line start with an open parenthesis and a letter and a close parenthesis
                            elif re.search(r"^\([a-z]\)", text[k+1].strip()):
                                f.write('\n')
                            # write '\n' only if the next line start "—"
                            elif re.search(r"^—", text[k+1].strip()):
                                f.write('\n')
                            # write '\n' only if the previous line start with a "-" and the next line do not start with a "-"
                            elif re.search(r"^—", text[k].strip()) and not re.search(r"^—", text[k+1].strip()):
                                f.write('\n')
                        f.close()
                    break
            break
    f.close()

    # creer un fichier xlsx nommé "excel_file" 
    with open('output.txt', 'r') as f:
        text = f.readlines()
        for i in range(len(text)):
            if '\n\n' in text[i]:
                text[i] = text[i].replace('\n', '')
                break
        f.close()

    df = pd.DataFrame(text, columns=["Articles"])
    excel_file = "output.xlsx"
    df.to_excel(excel_file, index=False)

    df = pd.read_excel('output.xlsx')
    df['Synapse Answers'] = ''
    df.to_excel('output.xlsx', index=False)
    
    #transform the first space in start_index to underscore
    start_index = start_index.replace(" ", "_")
    # remove the last caracter of start_index
    start_index = start_index[:-1]
    os.rename('output.xlsx', start_index + '.xlsx')
    # if the file named start_index + '.xlsx' is already in the folder 'result', remove it
    if os.path.exists('result/' + start_index + '.xlsx'):
        os.remove('result/' + start_index + '.xlsx')
    shutil.move(start_index + '.xlsx', 'result')
    
    os.remove('output.txt')

    print(f"{start_index}.xlsx se trouve maintenant dans le dossier 'result'")
