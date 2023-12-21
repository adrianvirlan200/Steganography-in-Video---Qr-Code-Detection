import string
from PIL import Image
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

def decode_message( image ):
    image_lsb_text = ''
    lsb_char_binary = ''
    end_of_message_string = '@#$%^&'

    for row in image:
        for pixel in row:
            b_steg = get_binary(pixel[0])
            g_steg = get_binary(pixel[1])
            r_steg = get_binary(pixel[2])
            
            if( len(lsb_char_binary) < 8 ): 
                lsb_char_binary += b_steg[-2]
                lsb_char_binary += b_steg[-1]
            else: 
                image_lsb_text += chr(int(lsb_char_binary, 2))
                lsb_char_binary = b_steg[-2]
                lsb_char_binary += b_steg[-1]

            if( len(lsb_char_binary) < 8 ): 
                lsb_char_binary += g_steg[-2]
                lsb_char_binary += g_steg[-1]
            else: 
                image_lsb_text += chr(int(lsb_char_binary, 2))
                lsb_char_binary = g_steg[-2]
                lsb_char_binary += g_steg[-1]

            if( len(lsb_char_binary) < 8 ): 
                lsb_char_binary += r_steg[-2]
                lsb_char_binary += r_steg[-1]
            else: 
                image_lsb_text += chr(int(lsb_char_binary, 2))
                lsb_char_binary = r_steg[-2]
                lsb_char_binary += r_steg[-1]
            
            if( (len(image_lsb_text) > 6) and ( image_lsb_text[-6:] == end_of_message_string )):
                return image_lsb_text[:-6]
    
    print('Nu a fost gasit separatorul de final!')

# elimina caracterele non-ascii(care nu sunt unicode), pentru a putea afisa string-ul
def remove_non_ascii(a_str):
    ascii_chars = set(string.printable)

    return ''.join(
        filter(lambda x: x in ascii_chars, a_str)
    )

orig_video = cv2.VideoCapture('new_3sec_video.avi')

frames = 10;

success,image = orig_video.read()
frames_count = 1;


text = ''
while success:
    if frames_count % 5 == 0 and frames_count <= frames * 5:
        text += decode_message(image)
        
    frames_count += 1
    success,image = orig_video.read()

# cateva carctere nu pot fi citite in unicode, le elimin
text = remove_non_ascii(text)

print(text)













