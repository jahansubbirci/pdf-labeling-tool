# ===== models/label.py =====

from typing import Tuple

class Label:
    '''Represents a single label with position and text'''
    
    def __init__(self, x: float, y: float, label_text: str, bbox: Tuple[float, float, float, float]):
        self.x = x
        self.y = y
        self.label_text = label_text
        self.bbox = bbox  # (x1, y1, x2, y2)
    
    def to_dict(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'label': self.label_text,
            'bbox': self.bbox
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Label':
        return cls(data['x'], data['y'], data['label'], tuple(data['bbox']))
    
    def __repr__(self):
        return f"Label('{self.label_text}' at {self.bbox})"
