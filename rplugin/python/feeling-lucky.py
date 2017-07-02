import neovim
import requests

@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.command('FeelingLuckyReflink', nargs='*')
    def feelingLuckyReflink(self, args):
        word = self.vim.eval('expand("<cword>")') 
        currentline = self.vim.current.line 
        self.vim.current.line = self.updateLine(currentline, word, 1)
    def updateLine(self, line, word, maxnum):
        if word in line:
            # get url
            var = requests.get(r'http://www.google.com/search?q="' + word + '"&btnI&pws=0&gl=us&gws_rd=cr')
            line = line.replace(word, '[' + word + '](' + var.url + ')', maxnum)
            #self.vim.command('echo "' + word + ", " + var.url + ", " + line + '"') # + args[0] + '"')
        return line


