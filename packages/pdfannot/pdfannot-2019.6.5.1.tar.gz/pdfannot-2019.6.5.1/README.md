
# pdfannot

This package aims to create a two-way link between annotated pdf and excel data frame.

It allows you to :

   - create an DataFrame containing each string annotated of the pdf in a column 'annot_text', along with its annotation in a column 'label' and information such as coordinates, page etc.
   - annotate a pdf given an DataFrame of the form described above.
   
It can be really useful for generating automatically annotated pdf documents with NLP models capable to
infer annotations from raw texts in a data frame.


### Prerequisites

- pandas
- fitz

(pip install pymupdf)



### Installing

pip install pdfannot


### Examples

Your DataFrame must contains info on what to annotate on the pdf :

    import pdfannot
    import pandas as pd
    
    # adf stands for annotation dataframe
    adf = pd.DataFrame([
    {'x': 40, 'y': 60, 'w': 300, 'h': 50}, 
    {'text': 'APPEAL relating to Cancellation Proceedings No 399', 'type': 'Highlight'},
    {'text': 'ication for a declaration of i', 'type': 'Highlight', 'label': 'label 1'},
    {'x': 100, 'y': 600, 'w': 300, 'h': 50, 'page': 1, 'label': 'label 2'}, 
     ])
    
    # pdfannot.exple_pdf is a test pdf shipped with pdf annot package / debug is set to True for some verbose
    pdfannot.annotate_pdf(adf, pdfannot.exple_pdf, '/tmp/test.pdf', debug=True)


    
Your annotation dataframe should have already columns 'x','y','h','w' (coordinate to make a square) or 'text' (texts to annotate).
   
    annotate_pdf(DataFrame, orig_pdfpath, dest_pdfpath)
    
will use your DataFrame and the directory of your pdf passed in argument to annotate it and store it at dest_pdfpath.

The function also considers optional columns 'label' to label your annotations and 'type' to specify whether you want 
a 'Square' or a 'Highlight'. 

Defaults are label : '' and type : 'Square'. 

Finally, specifying the annotation's page with a column 'page' speeds up the algorithm. "page" is optional for 1 page pdfs.


### Internals

However if your DataFrame has one text column per label of annotation (WARNING : each of them must be named annot_{label_name}) then you can transform it with :

    annot_utils.dlf2adf(DataFrame)

to make it acceptable by annotate_pdf. After this execute :

    annotate_pdf(DataFrame, orig_pdfpath, dest_pdfpath)

to annotate your pdf (this method allows only highlights).
    
    
### Authors

Arthur Renaud, Antoine Marullaz --> Stackadoc

Any recommendation/question ? --> contact@stackadoc.com 
