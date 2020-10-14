import numpy as np
import datetime
import random
class dataset:
    def __init__(self, filename):
        f = open(filename, "r", encoding="utf-8")
        self.sentences = []  # 所有的句子的集合
        self.tags = []  # 每个句子对应的词性序列
        sentence = []
        tag = []
        word_num = 0
        for i in f:
            if (i[0]!=" " and len(i) > 1):
                temp_tag = i.split()[3]#词性
                temp_word = i.split()[1]#单词
                sentence.append(temp_word)
                tag.append(temp_tag)
                word_num += 1
            else:
                self.sentences.append(sentence)
                self.tags.append(tag)
                sentence = []
                tag = []
        f.close()
        sentence_count = len(self.sentences)
        print("数据集%s中共有%d个句子，%d个词！" % (filename.split("/")[-1], sentence_count, word_num))

    def shuffle(self):
        temp=[(s,t) for s,t in zip(self.sentences,self.tags)]
        random.shuffle(temp)
        self.sentences=[]
        self.tags=[]
        for s, t in temp:
            self.sentences.append(s)
            self.tags.append(t)


class Linear_Model:
    def __init__(self,train_data,dev_data,test_data=None):
        self.train_set=dataset(train_data)
        self.dev_set=dataset(dev_data)
        if(test_data!=None):
            self.test_set=dataset(test_data)
        else:
            self.test_set=None
        self.feature_space={}
        self.tag_list=[]


    def create_feature_template(self,sentence,position,tag):
        temp_template=[]
        cur_word=sentence[position]
        cur_word_first_char=cur_word[0]
        cur_word_last_char=cur_word[-1]
        if(position==0):
            pre_word="$$"
            pre_word_last_word="$"
        else:
            pre_word=sentence[position-1]
            pre_word_last_word=pre_word[-1]
        if(position==len(sentence)-1):
            next_word="##"
            next_word_first_char="#"
        else:
            next_word=sentence[position+1]
            next_word_first_char=next_word[0]
        temp_template.append("02:"+tag+"-"+cur_word)
        temp_template.append("03:"+tag+"-"+pre_word)
        temp_template.append("04:"+tag+"-"+next_word)
        temp_template.append("05:"+tag+"-"+cur_word+"-"+pre_word_last_word)
        temp_template.append("06:"+tag+"-"+cur_word+"-"+next_word_first_char)
        temp_template.append("07:"+tag+"-"+cur_word_first_char)
        temp_template.append("08:"+tag+"-"+cur_word_last_char)
        for i in range(1,len(cur_word)-1):
            temp_template.append("09:"+tag+"-"+cur_word[i])
            temp_template.append("10:"+tag+"-"+cur_word_first_char+"-"+cur_word[i])
            temp_template.append("11:"+tag+"-"+cur_word_last_char+"-"+cur_word[i])
            if (cur_word[i]==cur_word[i+1]):
                temp_template.append("13:"+tag+'-'+cur_word[i]+'-'+'consecutive')
        if(len(cur_word)>1 and cur_word[0]==cur_word[1]):
            temp_template.append("13:"+tag+'-'+cur_word[0]+'-'+'consecutive')
        if(len(cur_word)==1):
            temp_template.append("12:"+tag+"-"+cur_word+"-"+pre_word_last_word+"-"+next_word_first_char)
        for i in range(0,4):
            if i>len(cur_word)-1:
                break
            temp_template.append("14:"+tag+"-"+cur_word[0:i+1])
            temp_template.append("15:"+tag+"-"+cur_word[-(i+1)::])
        return temp_template


    def create_feature_space(self):
        all_sentences=self.train_set.sentences
        all_tags=self.train_set.tags
        for i in range(len(all_sentences)):
            temp_sentence=all_sentences[i]
            temp_tag=all_tags[i]
            for j in range(len(temp_sentence)):
                temp_template=self.create_feature_template(temp_sentence,j,temp_tag[j])
                for k in temp_template:
                    if(k not in self.feature_space):
                        self.feature_space[k]=len(self.feature_space)
            for tag in temp_tag:
                if(tag not in self.tag_list):
                    self.tag_list.append(tag)
        print("整个特征空间总共有%d个特征"%len(self.feature_space))
        self.tag_list=sorted(self.tag_list)
        self.tag_dict = {t: i for i, t in enumerate(self.tag_list)}
        self.weight=np.zeros(len(self.feature_space),dtype="int32")
        self.v=np.zeros(len(self.feature_space), dtype="int32")

    #iterations表示需要进行多少次迭代，max_iterations表示多少次迭代对于准确率没有提升，则退出迭代，average_perceptron表示是否要用self.v代替self.weight，shuffle代表是否要打乱训练数据
    #只对dev开发集使用特征优化，对训练集不使用特征优化进行预测,使用self.weight进行预测.只是在学习的过程中不断地去更新self.v
    def Online_Training(self,iterations,max_iterations,average_perceptron,shuffle):
        train_sentences=self.train_set.sentences
        train_tags=self.train_set.tags
        max_accuracy_rate=0
        highest_accuracy_iterations=-1
        counter=0
        if(average_perceptron==True):
            print("在本次训练预测过程中使用self.v来代替self.weight对结果进行预测")
        else:
            print("在本次训练预测过程中使用self.weight对结果进行预测")
        for m in range(iterations):
            print("第%d轮迭代:" % (m+1))
            starttime=datetime.datetime.now()
            if(shuffle==True):
                print("在这一轮迭代中打乱所有的训练集数据！")
                self.train_set.shuffle()
                train_sentences = self.train_set.sentences
                train_tags = self.train_set.tags
            for j in range(len(train_sentences)):
                sentence=train_sentences[j]
                tags=train_tags[j]
                for i in range(len(sentence)):
                    correct_tag=tags[i]
                    predict_tag=self.predict(sentence,i,False)
                    if(correct_tag!=predict_tag):
                        feature_wrong=self.create_feature_template(sentence,i,predict_tag)
                        feature_correct=self.create_feature_template(sentence,i,correct_tag)
                        for f in feature_wrong:
                            if (f in self.feature_space):
                                self.weight[self.feature_space[f]]-=1
                        for f in feature_correct:
                            if (f in self.feature_space):
                                self.weight[self.feature_space[f]]+=1
                        if(average_perceptron):
                            self.v+=self.weight
            #评价程序
            train_correct_num,total_num,train_precision=self.evaluate(self.train_set,False)
            print('train(训练集)准确率：%d / %d = %f'% (train_correct_num, total_num, train_precision))
            dev_correct_num, dev_num, dev_precision = self.evaluate(self.dev_set, average_perceptron)
            print('dev(开发集)准确率：%d / %d = %f'%(dev_correct_num, dev_num, dev_precision))
            if(self.test_set!=None):
                test_correct_num, test_num, test_precision = self.evaluate(self.test_set, average_perceptron)
                print('test(测试集)准确率：%d / %d = %f' % (test_correct_num, test_num, test_precision))
            if dev_precision>max_accuracy_rate:
                max_accuracy_rate=dev_precision
                highest_accuracy_iterations=m
                counter=0
            else:
                counter+=1
            endtime = datetime.datetime.now()
            print("第%d次迭代所花费的时间为:%sS"%(m+1,endtime-starttime))
            if train_correct_num == total_num:
                break
            if(counter>=max_iterations):
                break
        print('第%d次迭代对应的开发集预测的准确率最高，最高的准确率为:%f'%(highest_accuracy_iterations+1,max_accuracy_rate))



    def calculate_score(self,features,averaged_perceptron):
        score=0
        for f in features:
            if(f in self.feature_space):
                if(averaged_perceptron==True):
                    score+=self.v[self.feature_space[f]]
                else:
                    score+=self.weight[self.feature_space[f]]
        return score

    def predict(self,sentence,position,average_perceptron):
        score=[]
        for tag in self.tag_list:
            template=self.create_feature_template(sentence,position,tag)
            score.append(self.calculate_score(template,average_perceptron))
        tag_num=int(np.argmax(score))
        return self.tag_list[tag_num]

    def evaluate(self,data_set,average_perceptron):
        all_sentence=data_set.sentences
        all_tag=data_set.tags
        total_num=0
        correct_num=0
        for i in range(len(all_sentence)):
            sentence=all_sentence[i]
            tag=all_tag[i]
            total_num+=len(tag)
            for j in range(len(sentence)):
                predict_tag=self.predict(sentence,j,average_perceptron)
                if(predict_tag==tag[j]):
                    correct_num+=1
        return (correct_num,total_num,correct_num/total_num)










