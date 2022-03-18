from pathlib import Path
from typing import Optional


class BBox:
    def __init__(
        self,
        image_path: Path,
        idx_to_class: dict,
        yolo_line: list,
        tags: Optional[dict] = None,
    ) -> None:
        self.image_path = image_path
        self.idx_to_class = idx_to_class
        self.tags = tags
        (
            self.class_idx,
            self.x_center,
            self.y_center,
            self.width,
            self.height,
            self.confidence,
        ) = self.preproces_line(yolo_line=yolo_line)
        self.class_name = self.idx_to_class[self.class_idx]
        self.check_values()

    def __repr__(self):
        return f"{self.bbox_class}-{self.x_center}-{self.y_center}-{self.width}-{self.height}-{self.confidence}"

    def preproces_line(self, yolo_line: list) -> dict:
        line = [round(float(num), 2) for num in yolo_line]
        return line[0], line[1], line[2], line[3], line[4], line[5]

    def get_coco(self):
        x_top_left = self.x_center - (self.width / 2)
        y_top_left = self.y_center - (self.height / 2)
        return {
            "bbox_class": self.bbox_class,
            "x_top_left": x_top_left,
            "y_top_left": y_top_left,
            "width": self.width,
            "height": self.height,
            "confidence": self.confidence,
        }

    def check_values(self):
        if self.x_center < 0:
            raise ValueError("x_center < 0")
        if self.y_center < 0:
            raise ValueError("y_center < 0")
        if self.width < 0:
            raise ValueError("width < 0")
        if self.height < 0:
            raise ValueError("height < 0")
        if self.confidence < 0:
            raise ValueError("confidence < 0")
        if isinstance(self.class_name, str):
            raise ValueError("self.class_name isnt str")
        
