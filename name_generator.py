import pandas as pd
import numpy as np
import json
from sex_classifier import SexClassifier
from argparse import ArgumentParser


class NameGenerater:

    def __init__(self, context_dict_path: str = 'context_dict.json', loc_prob_dict_path: str = 'loc_prob_dict.json') -> None:
        self.context_dict = NameGenerater.load_dict(context_dict_path)
        self.loc_prob_dict = NameGenerater.load_dict(loc_prob_dict_path)

    @staticmethod
    def get_names_from_csv(csv_path: str = 'names.csv'):
        data = pd.read_csv(csv_path)
        names = np.array(data)[:, 0]
        return names

    @staticmethod
    def get_all_family_names(names: list):
        family_names = set()
        for name in names:
            family_names.add(name[0])
        return family_names

    @staticmethod
    def get_all_chars(names: list):
        chars = set()
        for name in names:
            for c in name:
                chars.add(c)
        return chars

    @staticmethod
    def add_a_new_relation(d: dict, first_char: str, end_char: str):
        if first_char not in d.keys():
            d[first_char] = {end_char: 1}
        else:
            if end_char not in d[first_char]:
                d[first_char][end_char] = 1
            else:
                d[first_char][end_char] += 1
        return d

    @staticmethod
    def get_context_dict(names):
        '''
        key = char, value = dict
        value: key = char, value = number
        '''
        context_dict = {} 
        for name in names:
            for i, char in enumerate(name):
                if i == 0:
                    NameGenerater.add_a_new_relation(context_dict, '', name[0])
                elif i == len(name) - 1:
                    NameGenerater.add_a_new_relation(context_dict, name[i], '')
                else:
                    NameGenerater.add_a_new_relation(context_dict, name[i], name[i + 1])
        return context_dict

    @staticmethod
    def random_pick_a_key_from_freq_dict(freq_dict: dict):
        # 计算总出现次数
        number_sum = 0
        for char in freq_dict.keys():
            number_sum += freq_dict[char]
        # 计算概率：字的字典
        prob_dict = {}
        number_sum_now = 0
        for char in freq_dict.keys():
            number_sum_now += freq_dict[char]
            prob = number_sum_now / number_sum
            prob_dict[prob] = char
        # 按照概率随机找下一个字
        random_prob = np.random.random()
        for prob in prob_dict.keys():
            if random_prob < prob:
                return prob_dict[prob]


    def random_pick_next_char(self, first_char: str, allow_none=False):
        choices = dict(self.context_dict[first_char])
        if not allow_none and '' in choices.keys():
            choices.pop('')
        next_char = NameGenerater.random_pick_a_key_from_freq_dict(choices)
        return next_char

    @staticmethod
    def save_dict(d: dict, path: str = 'context_dict.json'):
        file = open(path, 'w', encoding='utf-8')
        content = json.dumps(d)
        file.write(content)
        file.close()

    @staticmethod
    def load_dict(path: str = 'context_dict.json'):
        file = open(path, 'r', encoding='utf-8')
        content = file.read()
        file.close()
        context_dict = json.loads(content)
        return context_dict

    def generate_a_random_name(self, length: int = 3):
        name = ''
        for i in range(length):
            if i == 0:
                next_char = self.random_pick_next_char('', allow_none=False)
            else:
                if name[-1] in self.context_dict.keys():
                    next_char = self.random_pick_next_char(name[-1], allow_none=False)
                    if next_char is None:
                        next_char = self.random_pick_a_key_from_freq_dict(self.loc_prob_dict[str(i + 1)])
                else:
                    next_char = self.random_pick_a_key_from_freq_dict(self.loc_prob_dict[str(i + 1)])
            name += next_char
        return name

    @staticmethod
    def get_loc_prob_dict(names):
        loc_prob_dict = {0: {}, 1: {}, 2: {}, 3: {}}
        for name in names:
            for i in range(len(name)):
                if name[i] in loc_prob_dict[i].keys():
                    loc_prob_dict[i][name[i]] += 1
                else:
                    loc_prob_dict[i][name[i]] = 1
        return loc_prob_dict

    @staticmethod
    def is_chinese_word(word: str):
        count = 0
        for s in word.encode('utf-8').decode('utf-8'):
            if u'\u4e00' <= s <= u'\u9fff':
                count += 1
        if count == len(word):
            return True
        else:
            return False

    def generate_many_names(self, sex=0, num=20, length=3):
        if length == 0:
            num_of_2 = np.random.randint(1, num)
            names = self.generate_many_names(sex, num_of_2, 2) + self.generate_many_names(sex, num - num_of_2, 3)
            np.random.shuffle(names)
            return names
            
        sex_classifer = SexClassifier()
        names = []
        while 1:
            name = self.generate_a_random_name(length=length)
            if not NameGenerater.is_chinese_word(name):
                continue
            cur_sex = sex_classifer.infer(name)
            if cur_sex == sex:
                names.append(name)
            if len(names) == num:
                return names

    @staticmethod
    def format_print(names, num_a_line=6):
        for i in range(len(names)):
            print(names[i], end='\t')
            if (i + 1) % num_a_line == 0:
                print('')


if __name__ == '__main__':
    parser = ArgumentParser(description='Name generator')
    parser.add_argument('--sex', type=int, default=0, help='0 means woman, 1 means man.')
    parser.add_argument('--num', type=int, default=20, help='Number of names. Must be in [2, 100]')
    parser.add_argument('--length', type=int, default=3, help='Number of characters of name. 2/3/0 is allowed. 0 means 2 or 3 are both ok')
    args = parser.parse_args()

    if args.sex not in [0, 1]:
        print('sex must be 0 or 1. 0 means woman, 1 means man.')
        exit()
    if args.length not in [2, 3, 0]:
        print('Wrong length:', args.length, 'Only 2, 3 or 0 is allowed')
        exit()
    if args.num <= 1 or args.num > 100:
        print('Num must be in [1, 100]')
        exit()

    name_generator = NameGenerater(context_dict_path='context_dict.json', loc_prob_dict_path='loc_prob_dict.json')
    names = name_generator.generate_many_names(sex=args.sex, num=args.num, length=args.length)
    NameGenerater.format_print(names)