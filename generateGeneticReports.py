from fpdf import FPDF
from geneSearch import GeneReport
import os
import argparse

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, label, 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, body):
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, body)
        # Line break
        self.ln()
        # Mention in italics
        #self.set_font('', 'I')
        #self.cell(0, 5, '(end of excerpt)')

    def Gene_Section(self,gene):
        self.chapter_title('Gene')
        self.set_font('Times', 'B', 12)
        self.multi_cell(0, 5, gene)
        self.ln()

    def Disease_Section(self, title, data):
        self.chapter_title(title)
        diseaseInfo = '\n'.join([i["diseaseName"] for i in data])
        self.chapter_body(diseaseInfo)

    def HPO_Section(self, title, data):
        self.chapter_title(title)
        for hpo in data:
            self.set_font('Times', 'B', 12)
            self.multi_cell(0, 5, hpo['name'])
            self.set_font('Times', '', 12)
            self.multi_cell(0, 5, hpo['definition'])
            self.ln()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('gene', nargs='*', metavar='N', type=str, help='Gene')
    res = parser.parse_args()
    if res.gene:
        testGenes = res.gene
    else:
        testGenes = ['ACTC','ATM','BRCA1','BRCA2','CACNA1A','CALR','CDH1','CFTR','CHEK2','CLCN1','CYP','DHCR7','EGFR','HEXA','HNF1A','KCNQ1','LDLR','LMNA','MMACHC','MYBPC3','PALB2','PFKM','PTEN','PYCR2','RAF1','SH2B3','SMAD4','SPATA7','STK11','TP53','TSC1','USH2A']
    title = 'Geneticheck - Genetic Report'
    pdfFolder = 'GeneticReports'
    if not os.path.exists(pdfFolder):
        os.mkdir(pdfFolder)

    for gene in testGenes:
        gn =  GeneReport(gene)
        pdf = PDF()
        pdf.set_title(title)
        pdf.set_author('Atilla Saadat')
        #pdf.print_chapter(2, 'THE PROS AND CONS', '20k_c2.txt')
        pdf.add_page()

        pdf.Gene_Section(gene)
        pdf.Disease_Section('Associated Diseases', gn.diseaseInfoDict)
        pdf.HPO_Section('Phenotype', gn.hpoAssociations)
        filePath = os.path.join(pdfFolder,'{}.pdf'.format(gene))
        pdf.output(filePath, 'F')
        print('Created',filePath)