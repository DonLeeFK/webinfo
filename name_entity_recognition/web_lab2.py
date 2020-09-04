import json
from sklearn_crfsuite import CRF
import pickle
import csv



def word_features(sent, i):
    word = sent[i]
    prev_word = "<s>" if i == 0 else sent[i-1]
    next_word = "</s>" if i == (len(sent)-1) else sent[i+1]
    features = {
        'w': word,
        'w-1': prev_word,
        'w+1': next_word,
        'w-1:w': prev_word+word,
        'w:w+1': word+next_word,
        'bias': 1
    }
    return features


def sent_features(sent):
    return [word_features(sent, i) for i in range(len(sent))]


class CRFModel(object):
    def __init__(self,
                 algorithm='lbfgs',
                 c1=0.14,
                 c2=0.15,
                 max_iterations=80,
                 all_possible_transitions=False
                 ):

        self.model = CRF(algorithm=algorithm,
                         c1=c1,
                         c2=c2,
                         max_iterations=max_iterations,
                         all_possible_transitions=all_possible_transitions)

    def train(self, sentences, tag_lists):
        features = [sent_features(s) for s in sentences]
        self.model.fit(features, tag_lists)

    def test(self, sentences):
        features = [sent_features(s) for s in sentences]
        pred_tag_lists = self.model.predict(features)
        return pred_tag_lists

doc=[]
train_word_list=[]
doc_len=[]
train_tag_list=[]
test_word_list=[]
test_tag_list=[]
test_doc_len=[]
pred_tag_list=[]
def input():
    global doc
    with open('subtask1_training_part1.json','r',encoding='utf-8') as f :
        for line in f.readlines():
            line = line.encode().decode('utf-8-sig')
            dic=json.loads(line)
            doc.append(dic)
def listtify():
    global doc
    for one_doc in doc:
        i=0
        str=one_doc['originalText']
        doc_len.append(len(str))
        for i in range(0,len(str)):
            train_word_list.append(str[i])
        for i in range(0,len(str)):
            train_tag_list.append('O')
    doc_num=0
    word_sum=0
    for one_doc in doc:
        label=one_doc['entities']
        for entity in label:
            label_type=entity['label_type']
            start_pos=entity['start_pos']
            end_pos=entity['end_pos']
            if(label_type=='实验室检验'):
                tag_tail='L'
            elif (label_type=='影像检查'):
                tag_tail='I'
            elif (label_type=='手术'):
                tag_tail='S'
            elif (label_type=='疾病和诊断'):
                tag_tail='D'
            elif (label_type=='药物'):
                tag_tail='M'
            else:
                tag_tail='A'
            tag_B='B'+'-'+tag_tail
            tag_I='I'+'-'+tag_tail
            tag_E='E'+'-'+tag_tail
            tag_S='S'+'-'+tag_tail
            if (end_pos==start_pos+1):
                train_tag_list[word_sum+start_pos]=tag_S
            else:
                for j in range(word_sum+start_pos,word_sum+end_pos):
                    if (j==word_sum+start_pos):
                        train_tag_list[j]=tag_B
                    elif (j==word_sum+end_pos-1):
                        train_tag_list[j]=tag_E
                    else:
                        train_tag_list[j]=tag_I
        word_sum=word_sum+doc_len[doc_num]
        doc_num=doc_num+1

def read_test_list():
    with open('实验二测试数据集.json','r',encoding='utf-8') as f :
        for line in f.readlines():
            dic=json.loads(line)
            str=dic['originalText']
            test_doc_len.append(len(str))
            for i in range(len(str)):
                test_word_list.append(str[i])
    print(test_word_list)


def save_model(model, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(model, f)

def crf_train_eval(remove_O=False):
    # 训练CRF模型
    global pred_tag_list
    crf_model = CRFModel()
    crf_model.train([train_word_list], [train_tag_list])
    save_model(crf_model, './trained_model/crf.pkl')
    pred_tag_list = crf_model.test([test_word_list])
    #print(pred_tag_list)
    #return pred_tag_list

def write_csv():
    f = open('output.csv','w+',encoding='utf-8',newline='')
    f_csv = csv.writer(f)
    header = ['textId','label_type','start_pos','end_pos']
    f_csv.writerow(header)
    doc_pos=0
    for j in range(0,len(test_doc_len)):
        for i in range(0,test_doc_len[j]):
            tag=pred_tag_list[0][i+doc_pos]
            label_type_full=''
            if(tag[0]=='B'):
                start_pos=i
                label_type=tag[2]
            if(tag[0]=='E'):
                end_pos=i+1
                if (label_type=='L'):
                    label_type_full='实验室检验'
                elif (label_type=='I'):
                    label_type_full='影像检查'
                elif (label_type=='S'):
                    label_type_full='手术'
                elif (label_type=='D'):
                    label_type_full='疾病和诊断'
                elif (label_type=='M'):
                    label_type_full='药物'
                else:
                    label_type_full='解剖部位'
                row = [str(j),label_type_full,str(start_pos),str(end_pos)]
                f_csv.writerow(row)
            if(tag[0]=='S'):
                start_pos=i
                label_type=tag[2]
                end_pos=i+1
                if (label_type=='L'):
                    label_type_full='实验室检验'
                elif (label_type=='I'):
                    label_type_full='影像检查'
                elif (label_type=='S'):
                    label_type_full='手术'
                elif (label_type=='D'):
                    label_type_full='疾病和诊断'
                elif (label_type=='M'):
                    label_type_full='药物'
                else:
                    label_type_full='解剖部位'
                row = [str(j),label_type_full,str(start_pos),str(end_pos)]
                f_csv.writerow(row)
        doc_pos=doc_pos+test_doc_len[j]
if __name__ == '__main__':
    input()
    listtify()
    read_test_list()
    crf_train_eval()
    write_csv()
    