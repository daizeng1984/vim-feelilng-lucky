import neovim

@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.function('FeelingLuckyReflink')
    def feelingLuckyReflink(self, args):
        self.vim.command('echo "hello from Feeling Lucky"')

