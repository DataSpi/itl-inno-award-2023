""" 
This file convert a .docx file to a .xlsx with file name, heading 1,2,3 as metadata. 
"""

import pandas as pd
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter


file_path="../../data/raw/6. HR.03.V3.2023. Nội quy Lao động_Review by Labor Department - Final.DOCX"
document_name = "HR.03.V3.2023. Nội quy Lao động"
# file_path="../../data/raw/10. HR.32.V4.2023. Thỏa ước Lao động tập thể-final.DOCX"
# document_name = "HR.32.V4.2023. Thỏa ước Lao động tập thể"
# file_path="../../data/interim/docx-edited/1. Healthcare Policy - V2 - final - VN.docx"
# document_name = "PO-ITL-HR-012. Healthcare Policy"
policy=docx.Document(file_path)

# store the paragraph objects into a dataframe for easily manipulation later. 
df=pd.DataFrame(policy.paragraphs, columns=["para_obj"])

# --------------------MANIPULATING--------------------
df['text']=[i.text.strip() for i in df.para_obj]
df['length']=df.text.str.len()
df['style_']=[i.style.name for i in df.para_obj]
df=df.query('length>0').reset_index(drop=True).drop(columns='para_obj')

# -----some data exploring. 
# df.style_.value_counts()
# df.style.format_index()
# df.length.plot(kind='hist') # check out if we have some too big paragraphs
# df.query('style_.str.contains("Heading")').style_.value_counts().sort_index()



# -----create column h1, h2, h3 filled with text from the text column. 
df['h1']=None
h1_rows = df.query("style_=='Heading 1'").index
df.loc[h1_rows, 'h1'] = df.loc[h1_rows, 'text']
df['h2']=None
h2_rows = df.query("style_=='Heading 2'").index
df.loc[h2_rows, 'h2'] = df.loc[h2_rows, 'text']
df['h3']=None
h3_rows = df.query("style_=='Heading 3'").index
df.loc[h3_rows, 'h3'] = df.loc[h3_rows, 'text']
df.query('style_.str.contains("Heading")') # just use this line to see the df & you'll know what's just happened


# -----ffill() for fill down the data (rows that do not have data will be filled by the value of the row above it.)
df.h1.ffill(inplace=True)
df.h2=df.groupby('h1')['h2'].transform(lambda x: x.ffill())
df.h3=df.groupby(['h1', 'h2'])['h3'].transform(lambda x: x.ffill())
df.head(50).style.background_gradient(subset='length') # see the df one more time. 


# -----remove some redundant rows
df2=df.query('~style_.str.contains("Heading")').fillna("").copy() # remove rows with _style.contains("Heading"), bc we've transfer these information to the cols [h1, h2, h3]
df3=df2.groupby(['h1', 'h2', 'h3'], sort=False)['text'].apply(lambda x: ' '.join(x))
df3=pd.DataFrame(df3)
df3['len']=df3.text.str.len()
df3.len.plot(kind='hist', title='Histogram of LEN before splitting text')

# -----split text of rows that have more than 600 characters.
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ".", ")", ";", ",", " ", ""],
    chunk_size=600,
    chunk_overlap=50,
    length_function=len
)
df3.loc[df3.text.str.len()>600, 'text'] = df3.text.apply(lambda x: text_splitter.split_text(x))
df3 = df3.explode('text') # Expanding the list into new rows
df3.reset_index(inplace=True)
df3['len2']=df3.text.str.len()
df3.drop(labels='len', axis='columns')
df3.len2.plot(kind='hist', title='Histogram of LEN after split text')
df3.style.format_index()


# merge the text of the heading to the body text. because the heading is meaningful for vectorization, so we need to include them in. 
df3.text = (df3.h1 + "/" + df3.h2  + "/" + df3.h3).str.rstrip("/") + ":\n" + df3.text
df3.len2 = df3.text.str.len()
# df3.style.format_index()



# -----saving
df3['document']=document_name
# df3[['document', 'h1', 'h2', 'h3', 'text']].to_excel('../../data/interim/nqld.xlsx', index=False)
# df3[['document', 'h1', 'h2', 'h3', 'text']].to_excel('../../data/interim/tuldtt.xlsx', index=False)
# df3[['document', 'h1', 'h2', 'h3', 'text']].to_excel('../../data/interim/healthcare.xlsx', index=False)

