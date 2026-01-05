import PyPDF2
import sys

def extract_text_from_pdf(pdf_path):
    """Extrait le texte d'un fichier PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
    except Exception as e:
        return f"Erreur lors de l'extraction: {e}"

if __name__ == "__main__":
    pdf_files = ["documentation-api-notion-compressed.pdf", "documentation-api-notion.pdf"]
    
    for pdf_file in pdf_files:
        print(f"\n{'='*60}")
        print(f"Analyse du fichier: {pdf_file}")
        print(f"{'='*60}")
        
        text = extract_text_from_pdf(pdf_file)
        
        if text.startswith("Erreur"):
            print(f"Échec: {text}")
        else:
            print(f"Nombre de pages: {len(PyPDF2.PdfReader(open(pdf_file, 'rb')).pages)}")
            print(f"Taille du texte: {len(text)} caractères")
            print(f"\nAperçu des premiers 2000 caractères:")
            print(f"{'-'*60}")
            print(text[:2000] + "..." if len(text) > 2000 else text)
            print(f"{'-'*60}")