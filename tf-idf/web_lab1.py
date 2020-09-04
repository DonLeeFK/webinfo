from pkuseg import pkuseg
import csv
from collections import Counter
# coding=utf-8

class text_lexicon:
    def __init__(self, id, df = 1， tf = 0):
        self.id = id
        self.df = df
    def __repr__(self):
        return '|term:{}, df:{}|'.format(self.id, self.df)



def segmentation(filename):
    title_list = []
    content_list = []
    seg = pkuseg(model_name="/Users/mac/WebInfo/web_lab1/mixed/")
    csv.field_size_limit(500*1024*1024)
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        text_row = next(reader)
        for text_row in reader:
            text_title = text_row[2]
            text_content = text_row[3]
            seg_title = seg.cut(text_title)
            #print(seg_title)
            title_list = insert(seg_title, title_list)
            seg_content = seg.cut(text_content)
            #print(seg_content)
            content_list = insert(seg_content, content_list)
    return title_list#, content_list

      
def insert(segs, working_list):
    word_list = working_list
    added_list = []
    for term in segs:
        flag = 1
        if term not in added_list:
            for i in range(len(word_list)):
                if term == word_list[i].id:
                    word_list[i].df += 1
                    flag = 0
                    added_list.append(term)
                    print('|{}:{}|'.format(word_list[i].id, word_list[i].df), end = ' ')
                    break
            if flag:
                word_list.append(text_lexicon(term, 1))
                added_list.append(term)
    return word_list

if __name__ == '__main__':
    filename = '文档数据集.csv'
    fout = open('out.txt','w')
    for lex in segmentation(filename):
        fout.write(str(lex))

    

      




