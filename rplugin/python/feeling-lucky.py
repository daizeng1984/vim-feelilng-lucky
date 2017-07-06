import neovim
import requests

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
        if not lines :
            word = self.vim.eval('expand("<cword>")') 
        else:
            # Quick fix...
            if len(lines) > 1 :
                lines[0] = lines[0][col1:]
                lines[-1] = lines[-1][:col2]
                word = "\n".join(lines)
            else:
                word = lines[0][col1:col2]
        currentline = self.vim.current.line 
        self.vim.current.line = self.updateLine(currentline, word, 1)
    def updateLine(self, line, word, maxnum):
        if word in line:
            # get url
            var = requests.get(r'http://www.google.com/search?q="' + word + '"&btnI&pws=0&gl=us&gws_rd=cr')
            line = line.replace(word, '[' + word + '](' + var.url + ')', maxnum)
            #self.vim.command('echo "' + word + ", " + var.url + ", " + line + '"') # + args[0] + '"')
        return line


