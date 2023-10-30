from langchain.document_loaders.word_document import Docx2txtLoader
import os


# Specify the folder path containing the .docx files
folder_path = "../../data/raw/"

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".docx"):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Load the .docx file
        loader = Docx2txtLoader(file_path=file_path)
        doc = loader.load()[0].page_content.lower()
        # print(doc)
        # Reduce multiple \n with one
        # doc=doc.replace('\n\t', '\n')
        # doc=re.sub(r"\n+", r"\n", doc)
        
        # print(f"----{filename}")
        # print(len(doc))
        # doc="\n".join(doc).lower()
        # print(doc)
        
        # Create the output file path
        output_file_path = os.path.join("../../data/processed/", f"{os.path.splitext(filename)[0]}.txt")
        
        # Write the modified content to a text file
        with open(output_file_path, "w") as file:
            file.write(doc)
