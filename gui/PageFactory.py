# import MeCab

class PageFactory(object):

    def __init__(self):
        # self._mc = MeCab.Tagger("-Ojrltoken")
        pass
    
    def GetPage(self):
        return """<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body style="background-color:#262626">

<h1>This is a Heading</h1>
<p>This is a paragraph.</p>
<a href="https://www.w3schools.com">This is a link</a> 

</body>
</html>"""