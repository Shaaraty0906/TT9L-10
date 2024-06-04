eng_dict = [] #list because to preserve word order

with open(r'words_with_freq.txt') as f:
    for line in f:
        val = line.rstrip('\n')
        eng_dict.append(val)
        
dict_by_len = {}

for v in eng_dict:
    word_only = v[0:v.find('---')]
    freq_only = int(v[v.find('---')+3:])
    word_len = len(word_only) # ignoring frequency while indexing words by length
    dist_let = ''.join(sorted(word_only)) #taking letters from word and sorting alphabetically 
    
    dict_by_len.setdefault(word_len, dict())
    dict_by_len[word_len].setdefault(dist_let, [])
    
    dict_by_len[word_len][dist_let].append((word_only, freq_only))
from PIL import Image, ImageFilter
import pytesseract as pt
pt.pytesseract.tesseract_cmd = r'D:\Programs\Tesseract-OCR\tesseract.exe'
import numpy as np
from ppadb.client import Client as AdbClient
import time
import os.path

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device = devices[0]
if len(devices) == 0:
    print('no device attached')
    quit()
def removeBlanks(image_arr, letter_height): 
    '''Function removes blank strips in between letters and returns imag without blank strips'''
    letter_width = 56
    gap_width = 40
    op_img = np.empty([62,78], dtype='uint8')
    start = 15
    
    for itr in range(6):           
        arr = image_arr[:letter_height, start:start+letter_width]
        op_img = np.append(op_img, arr, axis=1)
        start = start+letter_width+gap_width
    
    return op_img[:,79:]
def get_words_from_images():
    solve_for_screenshot = device.screencap() # get screenshot of image to solve

    img_dir = 'tryouts/'
    file_name = "4p1w-"+time.strftime("%Y%m%d-%H%M%S")
    img_save_path = os.path.join(img_dir, file_name+".png")

    with open(img_save_path, "wb") as fp:
        fp.write(solve_for_screenshot)

    img = Image.open(img_save_path) #get image
    img = img.convert('L') #convert to monochrome

    #Samsung A7
    left = 50
    upper = 1785 
    (left, upper, right, lower) = (left, upper, left+837, upper+240)
    img_crop = img.crop((left, upper, right, lower)) #crop the needed segment
    size = (561,160)
    img_crop = img_crop.resize(size)

    letter_height = 62 # height of each letter

    img_arr_test = np.array(img_crop) #convert image to numpy array
    
    img_arr_test[img_arr_test < 128] = 0    # to Black
    img_arr_test[img_arr_test >= 128] = 255 # to White
    
    img_arr_1 = img_arr_test[:letter_height,:] #top row image
    img_arr_2 = img_arr_test[letter_height+36:, :] #bottom row image

    words_from_images = pt.image_to_string(Image.fromarray(removeBlanks(img_arr_1, letter_height)), lang='eng', config='--psm 6')
    words_from_images += pt.image_to_string(Image.fromarray(removeBlanks(img_arr_2, letter_height)), lang='eng', config='--psm 6')
    
    words_from_images = (words_from_images.replace(' ','')).upper()
    
    return words_from_images, img_save_path, img
def solution_size():
    '''Get number of boxes (solution size) for this problem.'''
    b_left = 0
    b_upper = 1554 
    (b_left, b_upper, b_right, b_lower) = (b_left, b_upper, b_left+1080, b_upper+1) #only 1 pixel height
    box_img = img.crop((b_left, b_upper, b_right, b_lower))

    box_img.convert('L')

    bw_box = np.asarray(box_img).copy()

    bw_box[bw_box < 128] = 0    # to Black
    bw_box[bw_box >= 128] = 255 # to White

    previous = -1
    global box_start, box_count
    box_count = 0
    box_start = 9999 # To find where the box is starting - will be used to undo after wrong try
    for p in range(bw_box.shape[1]-1): # Count number of white pixels following a black pixel
        current = np.asscalar(bw_box[:,p:p+1])
        if previous==0 and current ==255:
            box_count += 1
            if box_start > p:
                box_start = p+55 # +55 so that we can do a 'jump' of equal length from start while undo
        previous = current
    
    return box_count-1
def get_possible_words_index():
    words_given = ''.join(sorted(words_from_images)) 
    word_len = box_count # boxes available in screenshot (solution size)

    possible_words_index = []

    for word_index in dict_by_len[word_len]: # To find all possible word indexes
        match_count = 0
        current_word_len = len(word_index)
        words_given_temp = words_given

        for w in word_index:
            if w not in words_given_temp:
                break
            if w in words_given_temp:
                match_count += 1
                words_given_temp = words_given_temp.replace(w, '', 1)

        if match_count == current_word_len:
            possible_words_index.append(word_index)
    
    return possible_words_index, word_len
def prepare_click_region():  
    click_region = dict()
    pos = 0
    for w in words_from_images:
        if w!='\n':
            click_region[pos] = w
            pos += 1
    return click_region
    
def get_click_pos(letter, click_region): 
    for key, value in click_region.items(): 
         if letter == value: 
            del click_region[key] # so we will get next elelemt position next time we search for same character
            if key <=5 :
                y = 1836
                x = 104+(148*key)
            else:
                y = 1975
                x = 104+(148*(key-6))
            return x,y,click_region
    return 50,1836
def check_success():
    '''Check if level is passed'''
    time.sleep(2) # Delay because the result is not shown immediately
    solve_for_solution = device.screencap() # get screenshot of image to solve

    img_dir_sol = 'checkIfSolve'
    file_name_sol = "4p1wCIS-"+time.strftime("%Y%m%d-%H%M%S")
    img_save_path_sol = os.path.join(img_dir_sol, file_name_sol+".png")

    with open(img_save_path_sol, "wb") as fp:
        fp.write(solve_for_solution)
        
    imgage_after_try = Image.open(img_save_path_sol) # Get image
    s_left = 0
    s_upper = 480
    (s_left, s_upper, s_right, s_lower) = (s_left, s_upper, s_left+1080, s_upper+1)
    imgage_after_try_arr = np.asarray(imgage_after_try.crop((s_left, s_upper, s_right, s_lower)))
    
    if np.average(imgage_after_try_arr[:,:,2]) == 28:
        return True
    else:
        x = box_start
        for b in range(box_count):
            y = 1550
            touch_coord_undo = 'input touchscreen tap {} {}'.format(x, y)
            device.shell(touch_coord_undo)
            x = x+110
        return False
def play():
    for word in possible_words:
        click_region = prepare_click_region()
        print(f"Now trying: ", word)
        for letter in word:
            x,y,click_region = get_click_pos(letter, click_region)
            touch_coord = 'input touchscreen tap {} {}'.format(x, y)
            device.shell(touch_coord)
        if(check_success()):
            device.shell("input touchscreen tap 532 1833") # click for next level
            break
# Play game   
while True:
    time.sleep(2)
    words_from_images, img_save_path, img = get_words_from_images()
    print(f'Words from image : ',words_from_images)

    box_count = solution_size()
    print(f'Box count : ',box_count)

    possible_words_index, word_len = get_possible_words_index()

    possible_words_unsort = []
    for i in possible_words_index:
        for j in dict_by_len[word_len][i]:
            possible_words_unsort.append(j)

    possible_words_sort = sorted(possible_words_unsort, key = lambda x : x[1], reverse=True)
    
    possible_words = []
    for w in possible_words_sort:
        possible_words.append(w[0])
    
    play()