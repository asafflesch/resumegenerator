from Cheetah.Filter import Filter

class HFilter(Filter):
	def filter(self, val, **kw):
        ''' Replace internal lists and explicit carriage returns with html syntax'''
        filtered = val.replace("{list}", "<ul>").replace("{/list}", "</ul>")
        filtered = filtered.replace("{item}", "<li>").replace("{/item}", "</li>")
        filtered = filtered.replace("{cr}", "<br>")
        return filtered

class LFilter(Filter):
	def filter(self, val, **kw):
        ''' Replace internal lists and explicit carriage returns with html syntax'''
        filtered = val.replace("{list}", "\begin{itemize}").replace("{/list}", "\end{itemize}")
        filtered = filtered.replace("{item}", "\item").replace("{/item}", "")
        filtered = filtered.replace("{cr}", "\\\\")
        return filtered
