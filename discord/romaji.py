from pykakasi import kakasi

class romaji():
  def __init__(self):
    self.kks = kakasi()
  
  def get_romaji(self, input: str) -> str:
    return ''.join([item['hepburn'] for item in self.kks.convert(input) if item['orig']]).replace('kitei','Kitty')
