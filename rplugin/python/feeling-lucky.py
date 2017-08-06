import neovim
import os 
import shelve
import re
from googleapiclient.discovery import build

class LuckyStay(object):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.db_path = dir_path + 'feelinglucky'

    # TODO: python2 problem with 'with'?
    def put(self, word, url):
        #with shelve.open(self.db_path) as db:
        db = shelve.open(self.db_path)
        db[word] = url
        db.close()

    def get(self, word):
        #with shelve.open(self.db_path) as db:
        #    return db[word]
        db = shelve.open(self.db_path)
        ret = db[word]
        db.close()
        return ret
        
    def getAll(self):
        #with shelve.open(self.db_path) as db:
        #    return dict(db)
        db = shelve.open(self.db_path)
        ret = dict(db)
        db.close()
        return ret


@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim
        self.luckyStay = LuckyStay();

    @neovim.command('FeelingLuckyReflink', nargs='*')
    def feelingLuckyReflink(self, args):
        buf = self.vim.current.buffer
        (lnum1, col1) = buf.mark('<')
        (lnum2, col2) = buf.mark('>')
        lines = self.vim.eval('getline({}, {})'.format(lnum1, lnum2))
        word = ""
        if lines :
            # Quick fix...
            if len(lines) > 1 :
                lines[0] = lines[0][col1:]
                lines[-1] = lines[-1][:col2]
                word = "\n".join(lines)
            else:
                word = lines[0][col1:col2]
        # Be smart
        if not word:
            word = self.vim.eval('expand("<cword>")') 
        currentline = self.vim.current.line 
        self.vim.current.line = self.updateLine(currentline, word, 1)
    def updateLine(self, line, word, maxnum):
        if word in line:
            self.service = build( 
                "customsearch", "v1",
                developerKey="AIzaSyCYtnzDWqzPYE6LTtNyuxEZ6pLy6DCkysQ")
            
            res = self.service.cse().list(
                    q=word,
                    cx='014324005263008877010:zmwtfjahkfe',
                    ).execute()
            url = ""
            if res :
                url = res.get('items', [{'link':''}])[0].get('link')

            # get url
            line = self.updateBuffer(line, word, url, maxnum)
            # upsert
            self.luckyStay.put(word, url)
            #self.vim.command('echo "' + word + ", " + var.url + ", " + line + '"') # + args[0] + '"')
        return line
    def updateBuffer(self, doc, word, url, maxnum):
        if not doc:
            return doc
        return re.sub(r"(" + word + ")", '[' + word + '](' + url + ')', doc, count=maxnum)

    @neovim.command('FeelingLuckyEverywhere', nargs='*')
    def luckyEveryWhere(self, args):
        d = self.luckyStay.getAll()
        i = 0
        # TODO: better to find all 
        taboo = []
        for l in self.vim.current.buffer:
            taboo = taboo + list(re.findall(r"(?:[[\s]*)([\S]+)(?:[\s]*])(?:[\s]*\([^)]*\))", l))
        for t in taboo:
            d.pop(t, None) 
        #self.vim.command('echo "lucky everywhere: ' + str(d) + '"')
        
        for l in self.vim.current.buffer:
            for word in d:
                l = self.updateBuffer(l, word, d[word], 1)
            #self.vim.command('echo "lucky everywhere: ' + str(l) + '"')
            if l != self.vim.current.buffer[i]:
                self.vim.current.buffer[i] = l;
                d.pop(word, None)
            i = i + 1



