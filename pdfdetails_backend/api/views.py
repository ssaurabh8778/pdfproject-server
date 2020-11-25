from django.http import JsonResponse
from PyPDF2 import PdfFileReader
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import io

#to the the api
def check(request):
    data = {
        'hello': 'world',
    }
    print(data)


    return JsonResponse(data)

#to send data back to frontend
def getFontData(request):

    link=io.BytesIO(request.FILES['file'].read())
    font1=getFontDetails(link)
    font2=getTextData(link)

    for i in range(0, len(font2)):
        for j in range(0, len(font1)):
            if (font2[i]['name'] == font1[j]['name']):
                font2[i]['embedded'] = font1[j]['embedded']

    pdf_length, pdf_info =getPdfInfo(link)
    data = {
        'pdf_length': pdf_length,
        'pdf_info':pdf_info,
        'font_details': font2,
    }
    return JsonResponse(data)




#method to get pdf length & pdf info
def getPdfInfo(link):
    pdf = PdfFileReader(link)
    pdf_length = pdf.getNumPages()
    pdf_info= pdf.getDocumentInfo()
    return pdf_length, pdf_info



#method to get sample text of each font
def getTextData(link):
    text_data = []

    def createPDFDoc(fpath):
        fp = fpath
        parser = PDFParser(fp)
        document = PDFDocument(parser, password='')
        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise "Not extractable"
        else:
            return document


    def createDeviceInterpreter():
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        return device, interpreter


    def parse_obj(objs):

        for obj in objs:

            if isinstance(obj, pdfminer.layout.LTTextBox):
                for o in obj._objs:
                    if isinstance(o,pdfminer.layout.LTTextLine):
                        text=o.get_text()
                        text_data.append({"name":"/"+o._objs[0].fontname, "text":text, 'embedded': 'No'})

            elif isinstance(obj, pdfminer.layout.LTFigure):
                parse_obj(obj._objs)
            else:
                pass


    document=createPDFDoc(link)
    device,interpreter=createDeviceInterpreter()
    pages=PDFPage.create_pages(document)
    x=[]
    for page in pages:
        interpreter.process_page(page)
        layout = device.get_result()
        parse_obj(layout._objs)

    text_data_sorted = sorted(text_data, key=lambda i: i['name'])

    K = "name"
    memo = set()
    filtered_data = []
    for sub in text_data_sorted:

        # testing for already present value
        if sub[K] not in memo:
            filtered_data.append(sub)

            # adding in memo if new value
            memo.add(sub[K])
    return filtered_data






#method to get font details
def getFontDetails(link):

    pdf = PdfFileReader(link)
    fonts = set()
    embedded = set()

    for page in pdf.pages:
        obj = page.getObject()
        f, e = walk(obj['/Resources'], fonts, embedded)
        fonts = fonts.union(f)
        embedded = embedded.union(e)

    unembedded = fonts - embedded
    font_data=[]

    if embedded:
        for i in embedded:
            font_data.append({"name":i, "text":"", "embedded":"Yes"})
    if unembedded:
        for i in unembedded:
            font_data.append({"name":i, "text":"", "embedded":"No"})

    font_data_sorted = sorted(font_data, key=lambda i: i['name'])

    return font_data_sorted


def walk(obj, fnt, emb):
    fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
    if '/BaseFont' in obj:
        fnt.add(obj['/BaseFont'])

    elif '/FontName' in obj and fontkeys.intersection(set(obj)):
        emb.add(obj['/FontName'])

    for k in obj:
        if hasattr(obj[k], 'keys'):
            walk(obj[k], fnt, emb)

    return fnt, emb