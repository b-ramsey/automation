from bs4 import BeautifulSoup
import requests
import io,sys,os

description = ""
bundles = ""

filePrefix = os.environ['HOME'].strip()
comment = '{1}Bundle \'{0}\' {1:>{width}}{2}\n'
bundler = 'Bundle \'{0}\'\n'

with open(filePrefix + '/.vim/bundle-names.list' , 'r') as f:
    for line in f:
        line_strip = line.strip()
        radj = 40 - len(line_strip)
        r = requests.get("https://www.github.com/"+line_strip)
        data = r.content
        soup = BeautifulSoup(data)
        div = soup.find(class_="repository-description")
        if div is not None:
            desc = div.contents[1]
            description += comment.format(line_strip, '"', desc.string, width=radj)
        else:
            description += line
        bundles += bundler.format(line_strip)
                                                                                                                            
#Sort description and bundles
desc_list = description.split('\n')
bund_list = bundles.split('\n')
                                                                                                    
desc_list.sort(key=str.lower)
bund_list.sort(key=str.lower)
                                                                                                                            
#Open file for writing
with open(filePrefix + '/.vim/plugins.vim', 'w') as f:
    for line in desc_list:
        f.write(line + '\n')

    f.write("\n\n\n\n\n")

    for line in bund_list:
        f.write(line + '\n') 
