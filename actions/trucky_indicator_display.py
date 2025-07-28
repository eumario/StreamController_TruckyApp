from .trucky_core import TruckyCore

class TruckyIndicatorDisplay(TruckyCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    def display_text(self, text, position: str = "bottom", size: int = None, outline_width: int = None):
        self.set_label(text=text, color=self.text_color, position=position, font_size=size, outline_width=outline_width)