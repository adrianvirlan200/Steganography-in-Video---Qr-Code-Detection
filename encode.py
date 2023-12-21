from PIL import Image
import pytesseract
import cv2
import numpy as np

def get_binary(message):
    if( type(message) == str ):
        binary_message = ( char.split('b')[1] for char in map(bin,bytearray(message,'utf8')) )
        binary_message_8b = []
        for binary_char in binary_message:
            to_fill = ''.join('0' for l in range(len(binary_char), 8))
            binary_message_8b.append((to_fill + binary_char))
        return ''.join(binary_message_8b)
    elif( type(message) == np.uint8 or type(message) == int  ):
        binary_message = bin(message).split('b')[1]
        to_fill = ''.join('0' for l in range(len(binary_message), 8))
        return to_fill + binary_message
    elif( type(message) == np.ndarray ):
        binary_message_8b = []
        for value in message:
            binary_message = bin(value).split('b')[1]
            to_fill = ''.join('0' for l in range(len(binary_message), 8))
            binary_message_8b.append(to_fill + binary_message)
        return ''.join(binary_message_8b)
    
def encode_message(image, message):
    end_of_message_string = '@#$%^&'
    message = message + end_of_message_string
    binary_message = get_binary(message)
    # print(">>>>>>>>>>>>>>>>")
    # print("message:",message)
    max_bytes_to_encode = ((image.shape[0] * image.shape[1] * 3 ) // 8 ) * 2
    if( max_bytes_to_encode > len(message) ):
        # Index pentru pozitia curenta din reprezentarea binara a mesajului
        index = 1
        for row in image:
            for pixel in row:
                b = get_binary(pixel[0])
                g = get_binary(pixel[1])
                r = get_binary(pixel[2])
                
                if( index < len(binary_message) ): 
                    b_steg = binary_message[index-1] + binary_message[index]
                    pixel[0] = int(b[0:-2] + b_steg, 2)
                    index += 2
                else: 
                    return image
                if( index < len(binary_message) ): 
                    g_steg = binary_message[index-1] + binary_message[index]
                    pixel[1] = int(g[0:-2] + g_steg, 2)
                    index += 2
                else: 
                    return image
                if( index < len(binary_message) ): 
                    r_steg = binary_message[index-1] + binary_message[index]
                    pixel[2] = int(r[0:-2] + r_steg, 2)
                    index += 2
                else: 
                    return image
    else:
        print("Mesajul este prea mare pentru a fi ascuns in imagine!")

    
# precizati calea catre executabil
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
# extrageti textul din imagine
img = Image.open('image.png')
text = pytesseract.image_to_string(img)
#sau
# text = pytesseract.image_to_string('image.png')

# scrieti rezultatul intr-un fisier
with open('text.txt', 'w') as f:
    f.write(text)

# folosesc acelasi videoclip de la punctul 2
orig_video = cv2.VideoCapture('3sec_video.avi')

fps = orig_video.get(cv2.CAP_PROP_FPS)
width = int(orig_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(orig_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Aleg secventa (5, 10, 15, ... 50) = 10 cadre
#calculez numarul caractere / cadru
frames = 10
# print('frames:', frames)
# print('nr_caractere:', len(text))
chars_per_frame = int(len(text) / frames) 
# print("nr_caractere/cadru:", chars_per_frame)

file=open("text.txt","r")
text = file.read()

# salvez video-ul nou intr-un format care nu afecteaza bitii(raw, necomprimat)
new_video = cv2.VideoWriter('new_3sec_video.avi', cv2.VideoWriter_fourcc(*'RGBA'), fps, (width, height))

# citesc fiecare cadru din video
success,image = orig_video.read()

frames_count = 1;
text_count = 0;
while success:
    if frames_count % 5 == 0 and frames_count <= frames * 5:
        image_stegano = encode_message(image, text[text_count*chars_per_frame:(text_count+1)*chars_per_frame])
        
        text_count += 1
        new_video.write(image_stegano[0:height, 0:width,:])
    else:
        new_video.write(image)
    frames_count += 1
    success,image = orig_video.read()


new_video.release()