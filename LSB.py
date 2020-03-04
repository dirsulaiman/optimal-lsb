"""
Last Significant Bit (LSB)

Implement the Optimal LSB algorihm on image

"""

import PIL.Image as image
import numpy as np


def lsb (target, data):
    """
    Embeded data to LSB of target
    ex: target='101010', data='111', return '101111'
    :param target: string <binary>
    :param data: string <binary>
    :returns: string
    """
    s1 = str(target)
    s2 = str(data)

    # check if data can't insert in target
    if len(s2)>len(s1):
        return target

    # lenght of data to insert
    n = len(s2)

    # slice a target
    s1 = s1[:-n]
    return s1+s2


def get_lsb (string, n):
    """
    Get LSB with lenght=n of string
    :param string: string
    :param n: integer
    :returns: string
    """
    return str(string[-n:])


def optimal_lsb (target, data):
    """
    Embeded data to LSB of target using Optimal LSB algorihm
    ex: target='101001', data='111', return '100111' not '101111'
    :param target: string <binary>
    :param data: string <binary>
    :returns: int
    """
    p = bin2dec(target)
    k = len(str(data))
    p_i = lsb(target, data)

    # Calculate value of Pi, Pi+, Pi-
    pi = bin2dec(p_i)
    p_pls = pi + 2**k
    p_neg = pi - 2**k
    return nearest([pi, p_pls, p_neg], p)
    # print(pi, p_pls, p_neg)
    # Find the Pi''
    #     if (abs(p-pi) <= abs(p-p_neg) <= abs(p-p_pls)) and (pi>=0 and pi<=255):
    #         return pi
    #     elif (abs(p-p_pls) <= abs(p-pi) <= abs(p-p_neg)) and (p_pls>=0 and p_pls<=255):
    #         return p_pls
    #     elif (abs(p-p_neg) <= abs(p-pi) <= abs(p-p_pls)) and (p_neg>=0 and p_neg<=255):
    #         return p_neg


def embed_str (filename, s):
    """
    Embeded string to image file.
    :param filename: string <file name with extension (ex. 'graybird.png')>
    :param s: string <binary without white space>
    :returns: PIL.Image <grayscale>
    """
    list_data = sliced(s, 3)

    image_target = image.open(filename).convert('L')
    image_array = np.array(image_target)

    image_array.shape
    index = 0

    new_image_array = image_array.copy()

    for i in range(len(image_array)):
        for j in range(len(image_array[0])):
            # print(index, list_data[index])
            new_image_array[i,j] = optimal_lsb(dec2bin(image_array[i,j]), list_data[index])
            if (index >= len(list_data)-1):
                break
            index = index+1
    return new_image_array


def stego (list_of_image, list_of_lsb):
    """
    Apply Optimal LSB algorihm to list of image
    :param list_of_image: list <string binary>
    :param list_of_lsb: list <string binary>
    :returns: list <integer>
    """
    m = list_of_image
    lsb = list_of_lsb
    # k = len(str(lsb[0]))
    len_lsb = len(lsb)
    len_m = len(m)
    for i in range(len_m):
        if i < len_lsb:
            m[i] = optimal_lsb(m[i], lsb[i])
        else:
            m[i] = bin2dec(m[i])
    return m


def lsb_from_image (filename, n):
    """
    Get LSB with lenght=n from each pixel value of an image
    :param filename: string <file name with extension (ex. 'bird.png')>
    :param n: integer <lenght of lsb>
    :returns: list of LSB <string>
    """
    list_lsb = []
    image_target = image.open(filename).convert('L')
    image_array = np.array(image_target)

    for i in range(len(image_array)):
        for j in range(len(image_array[0])):
            binn = set8bit(dec2bin(image_array[i,j]))
            value = get_lsb(str(binn), n)
            list_lsb.append(str(value))
    return list_lsb


def lsb_from_array (arr, n):
    """
    Get LSB with lenght=n from each element of an array 2D
    :param arr: array <int>
    :param n: integer <lenght of lsb>
    :returns: list of LSB <string>
    """
    list_lsb = []
    image_array = arr
    for i in range(len(image_array)):
        for j in range(len(image_array[0])):
            binn = set8bit(dec2bin(image_array[i,j]))
            value = get_lsb(str(binn), n)
            list_lsb.append(str(value))
    return list_lsb


def lsb_from_list_bin (l, n):
    """
    Get LSB with lenght=n from each element of list string
    :param l: list <string with binary number>
    :param n: integer <lenght of lsb>
    :returns: list of LSB <string>
    """
    result = []
    for i in l:
        i = set8bit(i)
        value = get_lsb(i, n)
        result.append(str(value))
    return result


def lsb_from_list_int (l, n):
    """
    Get LSB with lenght=n from each element of list integer
    :param l: list <integer>
    :param n: integer <lenght of lsb>
    :returns: list of LSB <string>
    """
    result = []
    for i in l:
        i = set8bit(dec2bin(i))
        value = get_lsb(i, n)
        result.append(str(value))
    return result


def dec2bin (x):
    """
    Convert integer to binary value
    :param x: integer
    :returns: string
    """
    return int(bin(x)[2:])


def bin2dec (s):
    """
    Convert binary value to integer
    :param s: string
    :returns: integer
    """
    s = str(s)
    return int(s,2)


def set8bit (s):
    """
    Set lenght of binner s to 8 bit, if s less than 8 bit then add zeros infront of s
    :param s: string
    :returns: string
    """
    n = len(str(s))
    if n>=8:
        return s
    less = 8-n
    zeros = ''
    for i in range(less):
        zeros = zeros + '0'
    return str(zeros+str(s))


def sliced (s, n):
    """
    Slice a string s to lenght=n of each element, if last sliced lenght less than n, then add zeros to last sliced until the lenght equal with n
    :param s: string
    :returns: list <string>
    """
    result = [s[0+i:n+i] for i in range(0, len(s), n)]
    # if last sliced lenght less than n, then add zeros to last sliced until the lenght equal with n
    if len(result[-1]) < n:
        less = n-len(result[-1])
        zeros = ''
        for i in range(less):
            zeros = zeros + '0'
        result[-1] = result[-1]+zeros
    return result


def remove_out_of_domain (l):
    """
    Remove list element that value < 0 or  value > 255
    :param l: list <number>
    :returns: list
    """
    new_list = l.copy()
    for i in range(len(l)):
        if l[i] > 255 or l[i] < 0:
            new_list.remove(l[i])
    return new_list


def nearest (list, value):
    """
    Find the smallest distance of each element in list to value
    :param list: list <number>
    :param value: integer
    :returns: integer <numpy.int64>
    """
    list = remove_out_of_domain(list)
    array = np.asarray(list)

    # find index of nearest list to value
    i = (np.abs(array-value)).argmin()
    return array[i]


def img2str (filename):
    """
    Convert an image grayscale to a string with binary number 8 bit
    :param filename: string <file name with extension (ex. 'bird.png')>
    :returns: string
    """
    img = image.open(filename).convert('L')
    arr = np.array(img)
    s = ''
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            bi = set8bit(dec2bin(arr[i,j]))
            s = s+str(bi)
    return s


def img2list_bin (filename):
    """
    Convert an image grayscale to a list string with binary number 8 bit
    :param filename: string <file name with extension (ex. 'bird.png')>
    :returns: list <string>
    """
    img = image.open(filename).convert('L')
    arr = np.array(img)
    result = []
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            value = set8bit(dec2bin(arr[i,j]))
            result.append(str(value))
            # print(type(result[i*len(arr)+j]))
    return result


def file2str (filename):
    """
    Convert an file text to a string, all newline are removed
    :param filename: string <file name with extension (ex. 'file.txt')>
    :returns: string
    """
    return open(filename,"r").read().replace('\n','')


def str2file (filename, s):
    """
    Save a string to text file
    If fine doesnt exist then create new file, if file exist replace contents of file
    :param filename: string <file name with extension (ex. 'file.txt')>
    :param s: string
    """
    f = open(filename,"w")
    # W = write new file, a='append existing file, new file if file does not exist'
    print(s, file=f)
    f.close()


def img_save(filename, arr):
    """
    Save array <numpy.array> to image
    If fine doesnt exist then create new file, if file exist replace file
    :param filename: string <file name with extension (ex. 'graybird.png')>
    :param arr: array 2D or more
    """
    img = image.fromarray(arr)
    img.save(filename)


def list2bin (l):
    """
    Convert list of integer to list of string binary
    :param l: list <integer>
    :returns: list <string 8 bit>
    """
    for i in range(len(l)):
        # print(type(l[i]))
        value = set8bit(dec2bin(l[i]))
        l[i] = str(value)
    return l


def list2str(l):
    """
    Convert list to a string
    :param l: list
    :returns: list <string>
    """
    s = ''
    for i in range(len(l)):
        s = s + str(l[i])
    return s


# convert array 2 dimension to list
# return as binary
def array2list(arr):
    """
    Convert array 2D to a list
    :param arr: array 2D
    :returns: list <string binary>
    """
    l = []
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            binn = dec2bin(arr[i,j])
            binn = set8bit(binn)
            l.append(str(binn))
    return l


def list2img(l, dim):
    """
    Make grayscale Image <PIL.Image> from list. If lenght of list not enough to make image with dimension = [high]*[width] then just return black imageself.
    Each pixel in image represented as integer with value 0~255 (8bit). If list given not 8 bit then the list is convert to a string and sliced to 8 bit of each element, it make the lenght of list may reducedself.
    :param l: list <string binary>
    :param dim: [high, width] <integer> (ex. dim=[100, 200]) or just [width] if width==high
    :returns: PIL.Image
    """
    if len(dim)==1:
        high = dim[0]
        width = dim[0]
    else:
        high = dim[0]
        width = dim[1]

    # if list not 8 bit, convert it to 8 bit by list2str() and sliced(list, 8)
    if len(l[0]) != 8:
        string = list2str(l)
        l = sliced(string, 8)

    m = np.zeros([high, width], dtype=np.uint8)
    # if lenght of list not enough to make image with dimension=dim, just return black image
    if len(l) < (high*width):
        print('len not enough')
        return image.fromarray(m)

    index = 0
    for i in range(high):
        for j in range(width):
            dec = bin2dec(l[index])
            index = index + 1
            m[i,j] = dec
    img = image.fromarray(m)
    return img


def str2list_bin (string):
    """
    Convert String to list <string binary>
    :param string: string
    :returns: list <string binary>
    """
    result = []
    arr = bytearray(string, encoding = 'utf-8')
    for i in arr:
        value = set8bit(dec2bin(i))
        result.append(value)
    return result


def list_bin2str (l):
    """
    Convert List <string binary> to a string
    :param l: list <string binary>
    :returns: string
    """
    result = ''
    for i in l:
        dec = bin2dec(i)
        value = chr(dec)
        result = result + str(value)
    return result


def printlist (l):
    s = ''
    for i in l:
        s = s + ' ' +str(i)
    print(s)


def compare_diff_of_list(l1, l2):
    """
    Compare the different value of 2 list. Lenght of both list must same
    :param l1: list
    :param l2: list
    foreach different value of elements l1 and elements l2 in same index
    :print(index, l1[i], l2[i])
    """
    if len(l1) != len(l2):
        print('Lenght not match')
        return
    count = 0
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            print( i, ', ', l1[i], l2[i])
            count = count + 1
    print('Total : ', count, ' different value')
