import os
def load_file(filename):
    """
    param: filepath
    retrun: textfile of string
    """
    file = open(filename, 'r')
    text = file.read()
    return text

def get_caption(filename):
    """
    param: takes filepath
    maps img_name to its 5 captions 
    retrun: dictionary """
    file = load_file(filename)
    captions = file.split('\n')
    descriptions ={}
    for caption in captions[:-1]:
        img, caption = caption.split('\t')
        if img[:-2] not in descriptions:
            descriptions[img[:-2]] = [ caption ]
        else:
            descriptions[img[:-2]].append(caption)
    return descriptions

import re
def clean_caption(descriptions):
    """
    param: dictonary (img_name mapped to its 5 captions)
    removes punctuation, numbers
    make all lowercase
    return: dictonary (img_name mapped to its 5 captions)
    """
    reg_exp = r'[^\w\s]'
    stop_words = ['s', 'a', 'an', 'the']
    for img, captions in descriptions.items():
        for i, caption in enumerate(captions):
            #removes punctuation
            caption = re.sub(reg_exp, ' ', caption)
            caption = caption.lower()
            token = caption.split()
            #removes hanging 's and articles
            token = [word for word in token if word not in stop_words]
            #remove numbers
            token = [word for word in token if(word.isalpha())]
            caption = ' '.join(token) 
            descriptions[img][i] = caption

    return descriptions

def text_vocab(descriptions):
    """
    params: dictonary (img_name mapped to its 5 captions)
    separte all unique words
    return: set of unique words
    """
    vocab = set()
    for key in descriptions.keys():
        [vocab.update(d.split()) for d in descriptions[key]]
    return vocab

def save_descriptions(descriptions, filename):
    """
    params: dictonary (img_name mapped to its 5 captions), new_filepath
    saves the cleans captions
    return: None
    """
    lines = []
    for img, captions in descriptions.items():
        for caption in captions:
            lines.append(img + '\t' + caption)
    data = "\n".join(lines)
    file = open(filename,"w")
    file.write(data)
    file.close()

#data directory
dataset_text_loc = 'D:\ml_datasets\Flickr8k_text'
dataset_image_loc = 'D:\ml_datasets\Flickr8k_Dataset'

#preparing our text data
filename = dataset_text_loc + "/" + "Flickr8k.token.txt"

#loading the file that contains all data
#mapping them into descriptions dictionary img to 5 captions
descriptions  = get_caption(filename)
print("Length of descriptions =" ,len(descriptions))

#cleaning the descriptions
clean_descriptions = clean_caption(descriptions)

#building vocabulary 
vocabulary = text_vocab(clean_descriptions)
print("Length of vocabulary = ", len(vocabulary))

#saving each description to file 
save_descriptions(clean_descriptions, "descriptions.txt")
