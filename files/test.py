import fitz  # PyMuPDF

def pdf_to_txt(input_pdf_path, output_txt_path):
    try:
        # Ouvrir le fichier PDF
        pdf_document = fitz.open(input_pdf_path)

        # Initialiser le texte extrait
        extracted_text = ""

        # Parcourir chaque page du PDF
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            extracted_text += page.get_text()

        # Écrire le texte extrait dans un fichier texte
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(extracted_text)

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

#parcourir le fichier et si on trouve la ligne "5.5.2017" supprimer les lignes suivantes jusqu'à ce que l'on tombe sur une ligne contenant"EN"
def remove_header_footer(input_txt_path, output_txt_path):
    should_remove = False
    with open(input_txt_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()
        i = 0
        while i < len(lines):
            if "5.5.2017" in lines[i]:
                should_remove = True
            if "EN" in lines[i]:
                should_remove = False
                lines[i] = ""
            if should_remove:
                lines[i] = ""
            i += 1
        txt_file.close()
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.writelines(lines)
        txt_file.close()


                
    


pdf_to_txt("pdf/Regulations.pdf", "text.txt")
remove_header_footer("text.txt", "text.txt")
