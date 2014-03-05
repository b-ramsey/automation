from bs4 import BeautifulSoup
import requests
import io,sys,os

def getDescription(url):
    r = requests.get(url)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        printError(e)
        raise Exception(e)
    except:
        raise
    
    data = r.content
    try:
        soup = BeautifulSoup(data)
    except HTMLParser.HTMLParseError as e:
        printError(e)
    except:
        raise

    return soup.find(class_="repository-description")


def printError(ex):
    try:
        sys.stderr.write('{0}({1}):\t{2}'.format(type(ex)._name_, ex.errno, ex.strerror))
    except AttributeError:
        sys.stderr.write('HTTP Error({0}): {1}'.format(ex.errno, ex.strerror))

def outputFile(desc, bundles ,filename=os.environ['HOME'].strip()+'/.vim/plugins.vim'):
    #Open file for writing
    try:
        f = open(filename, 'w')
    except OSError as e:
        printError(e)
        raise
    except:
        sys.stderr.write('Unexpected error has occured: exiting...')
        raise
    
    desc_list = desc.splitlines()
    bund_list = bundles.splitlines()

    for line in desc_list:
        f.write(line + '\n')
        print("Wrote: " + line )
    f.write("\n\n")

    for line in bund_list:
        f.write(line + '\n') 

def processFile(filename=os.environ['HOME'].strip()+'/.vim/bundle-names.list'):
    description = ""
    bundles = ""
    comment = '{1}Bundle \'{0}\' {1:>{width}}{2}\n'
    bundler = 'Bundle \'{0}\'\n'
   #Open the file for reading
    try:
        f = open(filename, 'r')
    except OSError as e:
        printError(e)
        raise
    except:
        raise

    for line in f:
        line_strip = line.strip()
        print("Getting info for: " + line_strip)
        radj = 40 - len(line_strip)
        url = "https://www.github.com/" + line_strip

        try:
            div = getDescription(url)
        except Exception as e:
            continue

        if div is not None:
            desc = div.contents[1]
            description += comment.format(line_strip, '"', desc.string, width=radj)
        else:
            description += line
        bundles += bundler.format(line_strip)
 
    return {
            'description' : description,
            'bundles'     : bundles
            }


def main():
    print("Getting info for bundle")
    procVal = processFile()

    print("Writing to file")
    outputFile(procVal['description'], procVal['bundles'])


main()
