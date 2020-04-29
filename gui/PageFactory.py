#!./python3env/bin/python3
import MeCab
from jamdict.util import Jamdict
import os

POS = {
    "名詞" : "noun",
    "助詞" : "particle",
    "動詞" : "verb",
    "接尾" : "suffix",
    "接続詞" : "conjunction",
    "助動詞" : "auxiliary",
    "形容詞" : "adjective",
    "副詞" : "adverb"
}
STYLE = "a.word:link {color: whitesmoke;text-decoration:none;} a.word:visited {color: whitesmoke;text-decoration:none;} a.word:hover {color: whitesmoke;text-decoration:none;font-weight:bold;}"

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
        if text == "":
            return self._template.format(
                    title=title, 
                    body="",
                    style=STYLE)
        if is_word:
            return self._template.format(
                title=title, 
                body="".join([PageFactory.paragraph("".join([PageFactory.paragraph(j) for j in entry])) for entry in self.words[text]]),
                style=STYLE)
        self.words = dict()
        tokens = [token.split("+-+")
                  for token in self._mc.parse(text).split("*+*")]
        tokens.pop()
        tokens.insert(0, ["U", "<p>"])
        tokens.append(["U", "</p>"])
        i = 0
        while i<len(tokens):
            if tokens[i][0][0].isspace():
                tokens[i][0] = tokens[i][0][1:]
                tokens.insert(i, ["U", " "])
                i += 1
            elif tokens[i][0][:2] == "\\n":
                tokens[i][0] = tokens[i][0][2:]
                tokens.insert(i, ["U", "</p><p>"])
                i += 1
            i += 1

        tokens = list(map(self._token_filter, tokens))

        body = []
        for token in tokens:
            if type(token[-1]) is int:
                if not token[-1] or token[3] == "記号":
                    body.append(token[0])
                    continue
                else:
                    lookup = self._jm.lookup(token[2], lookup_chars=False)
                    if len(lookup.entries) == 0:
                        result = f"Couldn&#39;t find {token[2]} in dictionary."
                        if "名" in token[-2]:
                            result += f" {token[2]} is a name according to MeCab."
                        self.words[token[2]] = [[result]]
                        body.append(self._wrap( token[0], token[2], "", result ))
                    else:
                        if len(lookup.entries) > 1:
                            priority_entries = []
                            for index, e in enumerate(lookup.entries):
                                for s in e.senses:
                                    if POS[token[3]] in s.pos or token[4] in POS and POS[token[4]] in s.pos:
                                        priority_entries.append(index)
                            lookup.entries = [*[lookup.entries[i] for i in priority_entries], 
                                              *[enum[1] for enum in filter(
                                                                    lambda x: x[0] not in priority_entries,
                                                                    enumerate(lookup.entries) )]]
                        self.words[token[2]] = list(map(PageFactory.entry_parse, lookup.entries))
                        body.append(self._wrap(
                            token[0], token[2], "",
                            "\n".join([e.text(False, " ", True) for e in lookup.entries])))
            else:
                lookup = self._jm.lookup(token[2], lookup_chars=False)
                if len(lookup.entries) == 0:
                    result = f"Couldn&#39;t find {token[2]} in dictionary."
                    if "名" in token[-1]:
                        result += f" {token[2]} is a name according to MeCab."
                    self.words[token[2]] = [[result]]
                    body.append(self._wrap(
                        token[0], token[2], PageFactory._swap_kat_to_hir(token[1]), result))
                else:
                    if len(lookup.entries) > 1:
                        priority_entries = []
                        for index, e in enumerate(lookup.entries):
                            for s in e.senses:
                                if POS[token[3]] in s.pos or token[4] in POS and POS[token[4]] in s.pos:
                                    priority_entries.append(index)
                        lookup.entries = [*[lookup.entries[i] for i in priority_entries], 
                                          *[enum[1] for enum in filter(
                                                                lambda x: x[0] not in priority_entries,
                                                                enumerate(lookup.entries) )]]
                    self.words[token[2]] = list(map(PageFactory.entry_parse, lookup.entries))
                    body.append(self._wrap(
                        token[0], token[2], PageFactory._swap_kat_to_hir(token[1]),
                        "\n".join([e.text(False, " ", True) for e in lookup.entries])))
        return self._template.format(
            title=title, 
            body="".join(body),
            style=STYLE)

    def _wrap(self, text, word, reading, short_info):
        return f"<ruby><a href='file://{self.parent.GetId()}/words/{word}' title='{short_info}' class='word'>{text}</a><rt>{reading}</rt></ruby>"


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
        token.extend(token.pop(3).split("|"))
        for char in token[0]:
            if PageFactory._is_kanji(char):
                return token
        return [*token, 1]

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
                if sense.pos:
                    result.append(f"<div style='text-indent:20px;'>part of speech: {' | '.join(sense.pos)}</div>")
                result.append(f"<div style='text-indent:20px;'>{i+1}. {' / '.join([str(g) for g in sense.gloss])}</div>")
        return result

    @staticmethod
    def paragraph(s):
        return f"<p>{s}</p>"
