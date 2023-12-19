import os
import json
from multiprocessing import Process
from tqdm import tqdm

from multiprocessing import Pool


class VocabCollector:
    def __init__(self, resource_paths):
        self.resource_paths = resource_paths
        self.batch_size = 1080
        self.vocabs = {}

    @staticmethod
    def clean_text(text):
        special_characters = '.,/?;:[]{}\\|`~!@#$%^&*()_+<>-=\\[\\]\'\"'
        text = text.replace('\n', '')
        for c in special_characters:
            text = text.replace(c, '')

        return text

    def get_resource(self, resource_path):
        with open(resource_path, 'r') as f:
            return f.readlines()
        
    def run(self, text):
        text = self.clean_text(text)
        words = text.split(' ')

        for i_w, word in enumerate(words):
            if i_w + 1 == len(words):
                break
            vocab = word + ' ' + words[i_w + 1]
            if vocab in list(self.vocabs.keys()):
                self.vocabs[vocab] = self.vocabs[vocab] + 1
            else:
                self.vocabs[vocab] = 1
        

    def __call__(self):
        for resource_path in self.resource_paths:
            resource = self.get_resource(resource_path)

            # processes = [Process(target=self.run, args=(text,)) for text in resource]
            # for p in tqdm(processes):
            #     p.start()
            # for p in processes:
            #     p.join()

            for i in tqdm(range(0, len(resource), self.batch_size)):
                processes = [Process(target=self.run, args=(text,)) for text in resource[i:i+self.batch_size]]
                for p in processes:
                    p.start()
                for p in processes:
                    p.join()

        with open('vocabs.json', 'w', encoding='utf-8') as f:
            json.dump(self.vocabs, f, ensure_ascii=False)


if __name__ == '__main__':
    resouce_paths = [
        'doc_layout_v1_processed.txt',
        'phomt.txt',
        'phomt_en.txt'
        ]
    
    vocabcollector = VocabCollector(resouce_paths)
    vocabcollector()