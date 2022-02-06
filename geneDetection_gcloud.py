from google.cloud import vision
import io
import os
import cv2
from google.cloud import vision
import io

def detect_text(path,gene):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    cvImage = cv2.imread(filePath)
    cvImageDir = 'detectedImages'
    if not os.path.exists(cvImageDir):
        os.mkdir(cvImageDir)

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    texts = response.text_annotations
    fullText = response.full_text_annotation.text
    for text in texts:
        if gene == text.description:
            vertices = text.bounding_poly.vertices
            offset = 2
            topLeft = (vertices[0].x-offset,vertices[0].y-offset)
            bottomRight = (vertices[2].x+offset,vertices[2].y+offset)
            cvImage = cv2.rectangle(cvImage, topLeft, bottomRight, (0, 255, 0), 2)

    cv2.imwrite(os.path.join(cvImageDir,os.path.basename(filePath)),cvImage)
    return fullText


def detect_document(filePath,gene):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(filePath, 'rb') as image_file:
        content = image_file.read()

    cvImage = cv2.imread(filePath)
    cvImageDir = 'detectedImages'
    if not os.path.exists(cvImageDir):
        os.mkdir(cvImageDir)

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    fullText = response.full_text_annotation.text

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            #print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                #print('Paragraph confidence: {}'.format(paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    if word_text == gene:
                        vertices = word.bounding_box.vertices
                        offset = 2
                        topLeft = (vertices[0].x-offset,vertices[0].y-offset)
                        bottomRight = (vertices[2].x+offset,vertices[2].y+offset)
                        cvImage = cv2.rectangle(cvImage, topLeft, bottomRight, (0, 255, 0), 2)
                    #print('Word text: {} (confidence: {})'.format(word_text, word.confidence))

                    #for symbol in word.symbols:
                    #    print('\tSymbol: {} (confidence: {})'.format(symbol.text, symbol.confidence))
    cv2.imwrite(os.path.join(cvImageDir,os.path.basename(filePath)),cvImage)
    return fullText

if __name__ == '__main__':
    folder = 'images'
    for filename in os.listdir(folder):
        filePath = os.path.join(folder,filename)
        gene = filename[:-4].split("_")[0]
        
        #fullText = detect_document(filePath,gene)
        fullText = detect_text(filePath,gene)
        
        if gene in fullText:
            print('PASSED - {} found in {}'.format(gene,filePath))
        else:
            print('FAILED - {} NOT found in {}'.format(gene,filePath))