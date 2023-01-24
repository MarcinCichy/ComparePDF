# gratulacje

# binary = '01100111 01110010 01100001 01110100 01110101 01101100 01100001 01100011 01101010 01100101'
# binary = '01100111011100100110000101110100011101010110110001100001011000110110101001100101'


def bin2txt(binary):
    count_spaces = 0
    sentence = ''
    for character in binary:
        if character.isspace():
            count_spaces = +1
    if count_spaces == 0:
        binary_list = [binary[i:i + 8] for i in range(0, len(binary), 8)]
        # print(binary_list)
    else:
        binary_list = binary.split()
        # print(binary_list)

    for i in range(0, len(binary_list)):
        data = int(binary_list[i], 2)
        char = chr(data)
        sentence += char
    return sentence

# print(bin2txt(binary))


def txt2bin(sentence):
    ascii_list =[]
    binary = []
    for letter in sentence:
        ascii_list.append(ord(letter))

    for i in range(0, len(ascii_list)):
        binary.append(bin(ascii_list[i]).replace("b", ""))
    return binary

