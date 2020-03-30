#!../python3env/bin/python3
import MeCab

class PageFactory(object):

    def __init__(self, parent):
        self.parent = parent
        self._mc = MeCab.Tagger("-Ojrltoken")
        with open("gui/view_template/testframe.html", "r") as view_template:
            self._template = view_template.read()
        self._is_kanji = lambda char: ord(char) > ord("\u4E00") and ord(char) < ord("\u9FBF")
        self._swap_kat_to_hir = lambda s : "".join([chr(ord(i)-0x60) for i in s])
        pass
    
    def _token_filter(self, token: list):
        if token[0] == 0:
            return [token[1], 0]
        for char in token[0]:
            if self._is_kanji(char):
                return token
        return [token[0], 0]
    
    
    def GetPage(self, title : str = "New Page",  text : str = "") -> str:
        tokens = [token.split("+-+") for token in self._mc.parse(text).split("*+*")]
        tokens.pop()
        i = 0
        while i<len(tokens):
            # sometimes mecab spits tokens like ' 数' that causes program to cut 
            # first char of furigana (while was necessary)
            if tokens[i][0][0].isspace():
                tokens[i][0] = tokens[i][0][1:]
                tokens.insert(i, ["U", " "])
                i += 1
            i += 1
        tokens = list(map(self._token_filter, tokens))

        body = []
        for token in tokens:
            if type(token[1]) is int:
                body.append(token[0])
            else:
                # TODO: Set up JMDict and make a page with it
                body.append(self._wrap(token[0], self._swap_kat_to_hir(token[1]), token[2])) 
        
        return self._template.format(title=title, body="".join(body),
         style="a.word:link {color: whitesmoke;text-decoration:none;} a.word:visited {color: whitesmoke;text-decoration:none;} a.word:hover {color: whitesmoke;text-decoration:none;font-weight:bold;}")
        "名前はヤロスラフ"


    def _wrap(self, text, reading, info):
        return f"<ruby><a href='file://{self.parent.GetId()}/words/a' title={info} class='word'>{text}</a><rt>{reading}</rt></ruby>"
    