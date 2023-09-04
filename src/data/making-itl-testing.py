import pandas as pd
%cd /Users/spinokiem/Documents/Spino_DS_prj/building_a_chatbot/

test_df = pd.read_csv('data/raw/itl-testing.csv')

test_df.instruction='"'+test_df.instruction+'"'
test_df['input']='"'+test_df['input']+'"'
test_df['output']='"'+test_df['output']+'"'
test_df.text='"'+test_df.text+'"'


test_df['text'] = ("Below is an instruction that describes a task. Write a response that appropriately completes the request. ### Instruction: " + 
                   test_df.instruction + "### Response: " + test_df.output
                   )
test_df.to_csv('data/raw/itl-testing.csv', index=False)

from datasets import load_dataset

dataset = load_dataset("vicgalle/alpaca-gpt4")