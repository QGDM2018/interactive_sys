"""
    the TF-IDF algorithm
"""
import jieba
import numpy as np

FUNCTION_NUM = 6

def cos_dist(vec1,vec2):
    """
    :param vec1:
    :param vec2:
    :return: cos_dist
    """
    if np.sum(vec1) == 0:
        return 0
    cos = float(np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return cos


def dataset(max_key_num=20, path='copus\\'):
    """

    :param max_key_num:
    :param path:
    :return:
    """
    global FUNCTION_NUM
    mapping = {0:'取款', 1:'存款', 2:'转账', 3:'查询余额', 4:'修改密码', 5:'打印账单'}
    # train = {
    #     0: ['取款', '取钱', '拿钱', '取款', '拿款', '拿现金', '取现金', '取', '拿', '现金', '支钱','拿出','支','出'],
    #     1: ['存款', '进钱', '存钱', '进款', '汇款', '存现金', '放现金', '进去', '打', '存', '放', '进去'],
    #     2: ['转账', '转钱', '转钱给别人', '拿钱给别人', '汇钱给他人', '汇钱给朋友', '转账给朋友', '汇'],
    #     3: ['查询余额', '查看余额', '查钱', '看钱', '多少钱', '有多少钱', '卡里有多少钱', '信息', '查',
    #         '个人', '账户','户头', '剩','剩多少','余额','余款'],
    #     4: ['修改密码', '改密码', '改码', '变密码', '换密码', '改', '变', '换', '密', '码', '别人知道我的卡', '风险', '危险'],
    #     5: ['打印账单', '看交易记录', '打印交易记录', '打印', '打', '印', '交易', '记录', '账单', '单', '帐']
    # }
    train = dict()
    for seq in range(FUNCTION_NUM):
        copus = open(path + str(seq) + '.txt', encoding='utf-8')
        contents = copus.readlines()
        train[seq] = eval(contents[0])


    for seq in range(len(train.keys())):
        cut_list = list()
        for word in train[seq]:
            sub_cut_list = jieba.lcut(word, cut_all=True)
            cut_list += sub_cut_list
        train[seq] = cut_list

    seq_counter = dict()
    for seq in range(len(train.keys())):
        word_counter = dict()
        for word in train[seq]:
            if word in word_counter.keys():
                word_counter[word] += 1
            else:
                word_counter[word] = 1
        seq_counter[seq] = word_counter

    # cal the tf
    seq_tf = dict()
    for seq in range(len(train.keys())):
        seq_tf[seq] = dict()
        len_tot_word = len(seq_counter[seq].values())
        for word in seq_counter[seq]:
            seq_tf[seq][word] = seq_counter[seq][word] / len_tot_word

    # cal the idf
    seq_idf = dict()
    for seq in range(len(train.keys())):
        seq_idf[seq] = dict()
        for word in seq_counter[seq]:
            tot_text_num = len(train.keys())
            in_text_num = 0
            for text in list(train.values()):
                if word in text:
                    in_text_num += 1
            seq_idf[seq][word] = np.log(tot_text_num / (in_text_num + 1))

    # cal the tf-idf
    seq_tf_idf = dict()
    for seq in range(len(train.keys())):
        seq_tf_idf[seq] = dict()
        for word in seq_counter[seq]:
            seq_tf_idf[seq][word] = seq_tf[seq][word] * seq_idf[seq][word]


    seq_counter_sort = dict()  #　reverse=True
    for seq in range(len(train.keys())):
        seq_counter_sort[seq] = sorted(seq_tf_idf[seq].items(), key=lambda x:x[1], reverse=True)

    now_min_key_num = 10000
    seq_sort = dict()
    Reserved_word = lambda x: x[0]
    for seq in range(len(train.keys())):
        seq_sort[seq] = list(map(Reserved_word, seq_counter_sort[seq]))
        seq_len = len(seq_sort[seq])
        # print(seq_len)
        if seq_len < now_min_key_num:
            now_min_key_num = seq_len

    max_key_num = now_min_key_num if now_min_key_num < max_key_num else max_key_num


    for seq in range(len(train.keys())):
        seq_sort[seq] = seq_sort[seq][:max_key_num]

    # print(seq_sort)

    return mapping, seq_sort, now_min_key_num


def text_match(sample):
    """

    :return:
    """
    sample_word = jieba.lcut(sample, cut_all=True)
    mapping, seq_sort, max_key_len = dataset()
    sample_len = len(sample_word)

    max_sim = -1
    sample_class = 0
    for seq in range(len(seq_sort.keys())):
        class_word = seq_sort[seq]
        set_word = list(set(sample_word + class_word))
        len_set_word = len(set_word)
        sample_vec = np.zeros(len_set_word)
        class_vec = np.zeros(len_set_word)
        for i in range(len_set_word):
            for j in range(sample_len):
                if sample_word[j] == set_word[i]:
                    sample_vec[i] += 1
            for k in range(len(class_word)):
                if class_word[k] == set_word[i]:
                    class_vec[i] += 1
        cos_sim = cos_dist(sample_vec, class_vec)
        print('---class %d---' % seq)
        print('sample_vec : %s' % str(sample_vec))
        print('class_vec  : %s' % str(class_vec))
        print('cos sim    : %f' % cos_sim)
        if max_sim < cos_sim:
            max_sim = cos_sim
            sample_class = seq

    if max_sim == 0:
        print('now nothing matches！')
        sample_class = 7
    else:
        print('final class : %s' % mapping[sample_class])

    return sample_class


















