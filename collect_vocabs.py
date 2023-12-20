from asyncio import as_completed, futures
from operator import le
import os
import resource
import time
import json
from multiprocess import Process, Manager
from multiprocessing import Pool
from regex import W
from tqdm import tqdm

import concurrent.futures

class VocabCollector:
    def __init__(self, resource_paths):
        self.resource_paths = resource_paths
        self.batch_size = 8
        self.vocabs = {}
        self.vocabs_as_list = []

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
            if vocab in list(self.vocabs_as_list):
                self.vocabs[vocab] = self.vocabs[vocab] + 1
            else:
                self.vocabs[vocab] = 1
                self.vocabs_as_list.append(vocab)

        return True
        # print(self.vocabs)
        

    # def collect(self):
    #     with Manager() as manager:
    #         self.vocabs = manager.dict(self.vocabs)
    #         for resource_path in self.resource_paths:
    #             resource = self.get_resource(resource_path)

    #             for i in tqdm(range(0, len(resource), self.batch_size)):
    #                 processes = [Process(target=self.run, args=(text,)) for text in resource[i:i+self.batch_size]]

    #                 for p in processes:
    #                     p.start()

    #                 for p in processes:
    #                     p.join()


    #     with open('vocabs.json', 'w', encoding='utf-8') as f:
    #         json.dump(self.vocabs.copy(), f, ensure_ascii=False)


if __name__ == '__main__':
    resouce_paths = [
        'doc_layout_v1_processed.txt',
        # 'phomt.txt',
        # 'phomt_en.txt'
        ]
    
    vocabcollector = VocabCollector(resouce_paths)
    # vocabcollector.collect()

    for resouce_path in resouce_paths:
        resource = vocabcollector.get_resource(resouce_path)
        
        with concurrent.futures.ThreadPoolExecutor() as exe:
            futures = {exe.submit(vocabcollector.run, resource[i]): i for i in tqdm(range(len(resource)))}

            for future in tqdm(concurrent.futures.as_completed(futures)):
                status = futures[future]

            with open('vocabs.json', 'w', encoding='utf-8') as f:
                json.dump(vocabcollector.vocabs.copy(), f, ensure_ascii=False)