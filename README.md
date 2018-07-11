# Singularity User Docs

This project uses <a href="http://docutils.sourceforge.net/rst.html"> reStructured Text (RST)</a> and <a href="https://readthedocs.org/">ReadTheDocs </a> . As a library for the current theme,  <a href="https://pypi.org/project/Sphinx/" alt="PyPI">Sphinx Python library </a> was used, using Python v. 2.7.
**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************
### I want to contribute, how can I set up my environment? ###


First things first, you will need to install the following tools:

- <a href="https://www.python.org/download/releases/2.7/">Install Python 2.7</a> 
- After that then you will need to install Sphinx:
  
```
pip install -U Sphinx
```

You're all set! after this you will only need to use your favorite editor for RST files.

### How to do stuff on RST? ### 

You can find a lot of information about RST on <a href="http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html">this site</a>

### How can I generate the html files once I have already edited the RST files? ### 

This is pretty straightforward by going to the root of the project on the command line and then do:

```
make html
```
This will generate a folder called **_build** which inside has the folder **html** containing all the html files needed.

### How to generate PDF files then? ### 

This is very similar to the previous step, you will need to execute on command line:

```
make latex
```
with this, a new folder inside **_build** will be generated, called **latex** and in there you can find the pdf file generated from RST (by default it is called "ReadTheDocsTemplate.pdf").

(Additional latex files are also generated if needed.)




