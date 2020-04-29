#!../python3env/bin/python3
import MeCab
from jamdict.util import Jamdict
import os


class PageFactory(object):

    def __init__(self, parent):
        self.parent = parent
        self._mc = MeCab.Tagger("-Ojrltoken")
        self._jm = Jamdict(db_file=os.path.join(
            os.path.dirname(__file__), "..", "jp-eng_dict", "Jamdict"))
        with open("gui/view_template/testframe.html", "r") as view_template:
            self._template = view_template.read()
        pass
    
    
    def GetPage(self, title: str = "New Page",  text: str = "", is_word=False) -> str:
        if is_word:
            return self._template.format(
                title=title, 
                body="".join([PageFactory.paragraph("".join([PageFactory.paragraph(j) for j in entry])) for entry in self.words[text]]),
                style="a.word:link {color: whitesmoke;text-decoration:none;} a.word:visited {color: whitesmoke;text-decoration:none;} a.word:hover {color: whitesmoke;text-decoration:none;font-weight:bold;}")
        self.words = dict()
        tokens = [token.split("+-+")
                  for token in self._mc.parse(text).split("*+*")]
        tokens.pop()
        tokens = list(map(self._token_filter, tokens))

        body = []
        for token in tokens:
            # TODO: Handle 助詞 and friends
            # TODO: Handle names (from Mecab)
            if type(token[1]) is int:
                if not token[1]:
                    body.append(token[0])
                else:
                    lookup = self._jm.lookup(f"{token[0]}", lookup_chars=False)
                    self.words[token[0]] = list(map(PageFactory.entry_parse, lookup.entries))
                    body.append(self._wrap(
                        token[0],
                        "",
                        "\n".join([e.text(False, " ", True) for e in lookup.entries])))
            else:
                lookup = self._jm.lookup(f"{token[0]}", lookup_chars=False)
                self.words[token[0]] = list(map(PageFactory.entry_parse, lookup.entries))
                body.append(self._wrap(
                    token[0],
                    PageFactory._swap_kat_to_hir(token[1]),
                    "\n".join([e.text(False, " ", True) for e in lookup.entries])))

        return self._template.format(
            title=title, 
            body="".join(body),
            style="a.word:link {color: whitesmoke;text-decoration:none;} a.word:visited {color: whitesmoke;text-decoration:none;} a.word:hover {color: whitesmoke;text-decoration:none;font-weight:bold;}")

    def _wrap(self, text, reading, short_info):
        return f"<ruby><a href='file://{self.parent.GetId()}/words/{text}' title='{short_info}' class='word'>{text}</a><rt>{reading}</rt></ruby>"


    @staticmethod
    def _swap_kat_to_hir(s):
        return "".join([chr(ord(i)-0x60) for i in s])
    
    @staticmethod
    def _is_kanji(char):
        return ord(char) > ord("\u4E00") and ord(char) < ord("\u9FBF")
    
    @staticmethod
    def _token_filter(token: list):
        if token[0] == "U":
            return [token[1], 0]
        for char in token[0]:
            if PageFactory._is_kanji(char):
                return token
        print(token)
        return [token[0], 1]

    @staticmethod
    def entry_parse(e):
        result = []
        if e.kana_forms:
            result.append("Kana forms: "+" / ".join([i.text for i in e.kana_forms]))
        if e.kanji_forms:
            result.append("Kanji forms: "+" / ".join([i.text for i in e.kanji_forms]))
        if e.senses:
            result.append("Senses: ")
            for i, sense in enumerate(e.senses):
                s = f"    {i+1}. {' / '.join([str(g) for g in sense.gloss])}" + \
                    (f" (part of speech: {' '.join(sense.pos)})" if sense.pos else "")
                print(s)
                result.append(s)
        print(result)
        return result

    @staticmethod
    def paragraph(s):
        return f"<p>{s}</p>"