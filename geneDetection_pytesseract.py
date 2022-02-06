from PIL import Image, ImageEnhance
import pytesseract
import numpy as np
import cv2
from IPython import embed
import os
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

folder = './images'
for filename in os.listdir(folder):
	filePath = os.path.join(folder,filename)
	gene = filename[:-4].split("_")[0]
	text = pytesseract.image_to_string(filePath)
	if gene in text:
		print('PASSED - {} found in {}'.format(gene,filePath))
	else:
		print('FAILED - {} NOT found in {}'.format(gene,filePath))
