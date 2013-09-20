from Cheetah.Filters import RawOrEncodedUnicode

''' Takes anything between every pair of {tagToReplace} and {\\tagToReplace} and turns it into <a href=content>content</a>, with an optional tagAddition before the content in the href'''
def ReplaceTagWithA(content, tagToReplace, tagAddition=""):
        count = content.count(tagToReplace)
        for curr in xrange(count):
                # Not-So-Beautiful Soup, but I don't want to use HTML tags
                startContent = content.find("{%s}" % tagToReplace) + len("{%s}" % tagToReplace)
                endContent = content.find("{\\%s}" % tagToReplace) 
                innerContent = content[startContent:endContent]
                content = content.replace("{%s}" % tagToReplace, "<a href = \" %s%s \">" % (tagAddition, innerContent) ,1)
                content = content.replace("{\\%s}" % tagToReplace, "</a>", 1)
        return content

class HFilter(RawOrEncodedUnicode):
        ''' Replace internal lists and explicit carriage returns with html syntax'''
	def filter(self, val, **kw):
                filtered = val.replace("{list}", "<ul>").replace("{\\list}", "</ul>")
                filtered = filtered.replace("{item}", "<li>").replace("{\\item}", "</li>")
                filtered = filtered.replace("{cr}", "<br/>")
                filtered = ReplaceTagWithA(filtered, "link")
                count = filtered.count("{email}")
                for curr in xrange(count):
                        # Making it possible to put an html email address on a public page without spam (spamspan, http://www.spamspan.com/, paranoia level 3)
                        startContent = filtered.find("{email}") + len("{email}")
                        endContent = filtered.find("{\\email}") 

                        innerContent = filtered[startContent:endContent]
                        filtered = filtered[:startContent] + filtered[endContent:]
                        strudelIndex = innerContent.find("@")
                        finalDotIndex = innerContent.rfind(".")

                        user = innerContent[0:strudelIndex]
                        servers = innerContent[(strudelIndex + 1) : finalDotIndex]
                        finalServers = innerContent[(finalDotIndex+1) : ]

                        tagReplacement = "<span class=\"spamspannerific\"> <span class=\"ssuc\"> %s </span> [at] <span class=\"ssdc\">%s [d0T] %s </span>" % (user, servers, finalServers)
                        filtered = filtered.replace("{email}", tagReplacement ,1)
                        filtered = filtered.replace("{\\email}", "</span>", 1)


                # If one is creating a private HTML file or otherwise does not mind the email address being public, you mark it with a publicemail tag and it's turned into a straight mailto link
                filtered = ReplaceTagWithA(filtered, "publicemail", "mailto:")
                filtered = filtered.strip()
                return filtered

class LFilter(RawOrEncodedUnicode):
        ''' Replace internal lists and explicit carriage returns with LaTeX syntax'''
	def filter(self, val, **kw):
                filtered = val.replace("{list}", "\\begin{itemize}").replace("{\\list}", "\\end{itemize}")
                filtered = filtered.replace("{item}", "\\item").replace("{\\item}", "")
                filtered = filtered.replace("{cr}", "\\\\")
                filtered = filtered.replace("#", "\#")
                filtered = filtered.replace("{link}", "")
                filtered = filtered.replace("{\\link}", "")
                filtered = filtered.replace("{email}", "\\mbox{\\small\\tt ")
                filtered = filtered.replace("{\\email}", "}")
                filtered = filtered.strip()
                return filtered
