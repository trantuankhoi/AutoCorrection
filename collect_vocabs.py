import os
from tqdm import tqdm
import json


class VocabCollector:
    def __init__(self, resource_paths):
        self.resource_paths = resource_paths
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
        
    def run(self):
        for resource_path in self.resource_paths:
            resource = self.get_resource(resource_path)

            for i, item in enumerate(tqdm(resource)):
                item = self.clean_text(item)
                words = item.split(' ')

                for i_w, word in enumerate(words):
                    if i_w + 1 == len(words):
                        break
                    vocab = word + ' ' + words[i_w + 1]
                    if vocab in list(self.vocabs.keys()):
                        self.vocabs[vocab] = self.vocabs[vocab] + 1
                    else:
                        self.vocabs[vocab] = 1

        # breakpoint()
        with open('vocabs.json', 'w', encoding='utf-8') as f:
            json.dump(self.vocabs, f, ensure_ascii=False)


if __name__ == '__main__':
    resouce_paths = ['/Users/KhoiTT/FTECH/01_Projects/TextOCR/AutoCorrection/phomt.txt']
    
    vocabcollector = VocabCollector(resouce_paths)
    vocabcollector.run()