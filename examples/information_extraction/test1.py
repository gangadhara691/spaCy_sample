import pyPdf

def getPDFContent(path):
    content = ""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(file(path, "rb"))
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
    # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content


print(getPDFContent("C:/Users/ssadanal/Desktop/python-spacy/pdf2txt/pdf/ar_2013_e.pdf").encode("ascii", "ignore"))


'''[
    'Net income was $9.4 million compared to the prior year of $2.7 million.Revenue exceeded twelve billion dollars, with a loss of $1b.',
    'Profits of capgemini for 2018 has crossed 1 million dollars with the total revenue of $1 billion',
]'''
