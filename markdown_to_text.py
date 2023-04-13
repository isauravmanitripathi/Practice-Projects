from bs4 import BeautifulSoup # This line imports the BeautifulSoup class from the bs4 module, which provides a way to parse and navigate HTML and XML documents.
from markdown import markdown # This line imports the markdown function from the markdown module, which converts Markdown-formatted text to HTML.
import re # This line imports the re module, which provides support for regular expressions in Python.

def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string) # This line uses the markdown() function to convert the input markdown_string to HTML, and assigns the resulting HTML string to the html variable.

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html) # This line uses the re.sub() function to remove any code snippets (text enclosed in <pre> and </pre> tags) from the html string. The resulting string is assigned back to the html variable.
    html = re.sub(r'<code>(.*?)</code >', ' ', html) # This line uses the re.sub() function to remove any inline code blocks (text enclosed in <code> and </code> tags) from the html string. The resulting string is assigned back to the html variable.
    html = re.sub(r'~~(.*?)~~', ' ', html) # This line uses the re.sub() function to remove any strikethroughs (text enclosed in ~~ characters) from the html string. The resulting string is assigned back to the html variable.

    # extract text
    soup = BeautifulSoup(html, "html.parser") # This line uses the BeautifulSoup() function from the bs4 module to parse the html string and create a BeautifulSoup object called soup. This object represents the HTML document as a tree of nested tags.
    text = ''.join(soup.findAll(text=True)) # This line uses the findAll() method of the soup object to find all text nodes in the HTML document, and concatenates them into a single string. The resulting string is assigned to the text variable.

    return text # This line returns the text variable, which contains the plaintext content of the original Markdown string.