# ===== core/label_manager.py =====

import json
from typing import Dict, List
from models.label import Label

class LabelManager:
    '''Manages labels for all pages'''
    
    def __init__(self):
        self.labels: Dict[int, List[Label]] = {}
    
    def add_label(self, page_num: int, label: Label):
        '''Add a label to a specific page'''
        if page_num not in self.labels:
            self.labels[page_num] = []
        self.labels[page_num].append(label)
    
    def get_labels(self, page_num: int) -> List[Label]:
        '''Get all labels for a specific page'''
        return self.labels.get(page_num, [])
    
    def delete_label(self, page_num: int, index: int):
        '''Delete a label by index from a specific page'''
        if page_num in self.labels and 0 <= index < len(self.labels[page_num]):
            del self.labels[page_num][index]
    
    def clear_page(self, page_num: int):
        '''Clear all labels from a specific page'''
        if page_num in self.labels:
            self.labels[page_num] = []
    
    def clear_all(self):
        '''Clear all labels from all pages'''
        self.labels = {}
    
    def get_total_labels(self) -> int:
        '''Get total number of labels across all pages'''
        return sum(len(labels) for labels in self.labels.values())
    
    def save_to_file(self, file_path: str):
        '''Save labels to JSON file'''
        data = {}
        for page_num, labels in self.labels.items():
            data[str(page_num)] = [label.to_dict() for label in labels]
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, file_path: str):
        '''Load labels from JSON file'''
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        self.labels = {}
        for page_num_str, labels_data in data.items():
            page_num = int(page_num_str)
            self.labels[page_num] = [Label.from_dict(ld) for ld in labels_data]
# ====================