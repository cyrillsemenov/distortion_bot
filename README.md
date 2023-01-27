# Distortion bot

> **Warning**
>
> Please be aware that the bot is intended for adult audiences and contains explicit content. Use it at your own risk.

This is a simple echo bot that echoes any incoming text messages in a distorted way.

The bot uses the text_distort module to replace words in the incoming message with words are read from a file, which is a list of words.

To start this bot just fill [`.env`](.env.example) file and then run:
``` bash
pip install -r requirements.txt
python main.py
```

The bot will start polling for updates and will respond to any incoming text messages.

You can also customize the behavior of the bot by [adjusting the parameters of the TextDistort class](#text-distortion) in the [`main.py`](main.py) file.

It is worth noting that the bot uses a proxy if the environment variable `'PYTHONANYWHERE_SITE'` is set.

---

## Text Distort class

### Overview
This class is used to create a text distortion effect by using a given dictionary file as a reference.

It compares words in the text to be distorted with the words in the dictionary file, 
and if there is a match within a specified Levenshtein distance threshold, 
it substitutes the word in the text with a similar word from the dictionary.

The class utilizes a substring matching technique to optimize the search process and minimize the computation time.

Method `__call__(self, string: str)` takes a string as an input and returns the distorted text.

---

### Usage
```python
from text_distort import TextDistort

distort = TextDistort(db_path='path/to/dictionary.txt', threshold=6, substring_length=2)
distorted_text = distort('This is a test text')
```

---

### Parameters
- `db_path`: path to text file with list of words.
- `threshold`: maximal Levenshtein distance to substitute words.
- `substring_length`: length of the substrings that are taken from the beginning and end of each word when the database is created.
