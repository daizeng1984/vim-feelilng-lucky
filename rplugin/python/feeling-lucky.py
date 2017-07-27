import neovim
from googleapiclient.discovery import build

@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

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
            line = line.replace(word, '[' + word + '](' + url + ')', maxnum)
            #self.vim.command('echo "' + word + ", " + var.url + ", " + line + '"') # + args[0] + '"')
        return line


