# class SexClassifier:


import random
import nltk
import pandas as pd
from pathlib import Path
from numpy import mean
import pickle

current_path = Path.cwd()



class SexClassifier:
    def __init__(self) -> None:
        self.classifier = SexClassifier.load_model()
    

    def save_model(classifier, path: str = 'sex_classifier.pickle'):
        f = open(path, 'wb')
        pickle.dump(classifier, f)
        f.close()

    def load_model(path: str = 'sex_classifier.pickle'):
        f = open(path, 'rb')
        classifier = pickle.load(f)
        f.close()
        return classifier

    # 特征提取
    @staticmethod
    def gender_features(name):
        name = name.lower()
        if len(name) == 2:
            return {
                'last_name': name[-1]
            }
        if len(name) >= 3:
            return {
                'last_name': name[-1],
                'last2_name': name[-2],
                'last12_name': name[-2:]
            }

    # 获取featuresets
    @staticmethod
    def get_featuresets(X, y):
        labeled_names = []
        for i in range(len(X)):
            labeled_names.append((X.values[i], y.values[i]))

        # 数据打乱
        random.shuffle(labeled_names)
        # 我们使用特征提取器来处理数据
        featuresets = [(SexClassifier.gender_features(name), gender) for (name, gender) in labeled_names]
        return  featuresets

    def infer(self, name: str):
        return self.classifier.classify(SexClassifier.gender_features(name))
    
    @classmethod
    def train(cls, data_path: str = 'name_gender_clear.csv'):
        df = pd.read_csv(Path(current_path, 'name_gender_clear.csv'), encoding='utf8')
        featuresets_train = cls.get_featuresets(df['name'], df['sex'])
        classifier = nltk.NaiveBayesClassifier.train(featuresets_train)
        cls.save_model(classifier)


if __name__=='__main__':
    sex_classifier = SexClassifier()
    mode = 'test'
    if mode == 'train':
        sex_classifier.train()
    else:
        print(sex_classifier.infer('貂蝉'))
        exit()