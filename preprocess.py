import pandas as pd
import operator
import os
import re


def judgeRepeat(L1, L2):
    if len(L1) != len(L2):
        return False
    else:
        return operator.eq(L1, L2)


def compressed(commentList):
    #     初始化两个空列表
    L1 = []
    L2 = []
    compressList = []  # 机械压缩去词后的评论列表
    #     循环评论列表的每一个单词进行判断
    for letter in commentList:
        if len(L1) == 0:  # 如果L1为空，直接将字符放入列表1中
            L1.append(letter)
        else:
            if L1[0] == letter:  # 列表1不为空，第一个列表的第一个字符和读入相同
                if len(L2) == 0:
                    L2.append(letter)  # 如果L2为空，放入L2中
                else:
                    #                     L2也有字符，触发压缩判断，如果得到重复
                    if judgeRepeat(L1, L2):
                        #                         进行压缩去除，清空第二个列表，将这个单词放到清空之后的第二个列表中
                        L2.clear()
                        L2.append(letter)
                    else:
                        #                         L1和;L2 不重复，则清空两个列表，
                        # 清除之前把两个列表的内容放入到最终的列表中，然后将当前单词放入到第一个列表的第一个位置
                        compressList.extend(L1)
                        compressList.extend(L2)
                        L1.clear()
                        L2.clear()
                        L1.append(letter)

            else:
                #                 当前读入的字符和第一个列表的首字符不相同
                # 触发压缩判断，如果得出重复，并且列表含的字符长度大于等于2
                if judgeRepeat(L1, L2) and len(L2) >= 2:
                    #                 则进行压缩去除，清空两个列表，把读入的这个字符放入第一列表第一个位置
                    compressList.extend(L1)
                    L1.clear()
                    L2.clear()
                    L1.append(letter)
                else:
                    #                 如果得不出重复，且第二个列表没有放入字符中，则继续在第一个列表中放入当前的数据
                    if len(L2) == 0:
                        L1.append(letter)
                    else:
                        #                     如果得不出重复，且第二列表已经放入了字符，则在第二个列表中放入当前字符
                        L2.append(letter)
    else:
        # 规则7：读完所有字符后，触发压缩判断，对list1以及list2有意义部分进行比较，若得出重复，则进行压缩去除。
        if judgeRepeat(L1, L2):
            compressList.extend(L1)
        else:
            compressList.extend(L1)
            compressList.extend(L2)
    L1.clear()
    L2.clear()
    return compressList





#name='一加'
#name='小米'
#name='华为'
#name='vivo'
#name='Oppo'
name='Apple'

#抽取
inputfile = '京东_手机_'+name+'_评论.csv'
data = pd.read_csv(inputfile,encoding='utf-8',header=None)
data1=data[2]
data1.to_csv('京东_手机_'+name+'_评论_抽取.txt',index=False,header=False)

#文本去重
data2 = pd.read_csv('京东_手机_' + name + '_评论_抽取'+'.txt',encoding='utf-8',header=None)
len1 = len(data2)
print(u"原始评论数据有%d" % len1)
data3 = pd.DataFrame(data2[0].unique())
# 记录去重后的评论数量
len2 = len(data3)
print(u"去重后的数据有%d条" % len2)
# 将去重后的数据写入文档中
data3.to_csv('京东_手机_'+name+'_评论_抽取_去重.txt',header=False,index=False,encoding='utf-8')
print("删除了%d条评论数据" %(len1-len2))

#机械压缩&短评删除
data4 = pd.read_csv('京东_手机_'+name+'_评论_抽取_去重.txt',encoding='utf-8',header=None)
comments = data4[0].values
compcomms = []
for comment in comments:
#         将评论文本转换成字符串，对每个评论进行处理，删除小于等于四个字符的评论数据
    comm = str(comment)
    if len(comm)<=4:
        pass
    else:
#             使用正则表达式删除所有的标点符号和空格
        comm = re.sub("[\s+\.\!V,$%^*(+\"\"]+|[-+!,.?、~@#$%......&*();`:]+","",comm)
#     将每条评论数据转换为字符列表
        commList = list(comm)
        compList = compressed(commList) #压缩前缀重复
        compList = compressed(commList[::-1]) #压缩后缀重复
        compList = compList[::-1]#把已经反转的列表再转置回来
#           压缩后的评论再进行短语删除
        if len(compList)<=4:
            pass
        else:
#                 将压缩后的评论列表转换成字符串并构造成DataFrame的格式
            compcomm = []
            compcomm.append("".join(compList))
            compcomms.append(compcomm)
else:
#   将compcomms数据转换为数据框DataFrame
    compcomms = pd.DataFrame(compcomms)
    compcomms.to_csv('京东_手机_'+name+'_评论_抽取_去重_机械压缩&短评删除.txt',index=False,header=False,encoding='utf-8')
print(compcomms)