import requests


# ------------------------UPLOAD VIA URLS------------------------
def get_src_id_pdf_url(file_name, url, api_key):
    headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
    }

    # this is the url that leads to pdf you need to read
    data = {'url': url}

    # do a response request
    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-url', headers=headers, json=data)

    if response.status_code == 200:
        print('Source ID:', response.json()['sourceId'])
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
    return {file_name: response.json()['sourceId']}
    # this is succeed so I get this line: "Source ID: src_Arsacx2vZLICB1FH9f2lF"



# ------------------------UPLOAD VIA FILES------------------------
def get_src_id_pdf_file(file_name, file_path, api_key):
    files = [
        ('file', (file_name, open(file_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': api_key
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    if response.status_code == 200:
        print('Source ID:', response.json()['sourceId'])
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
    return {file_name: response.json()['sourceId']}

api_key = 'sec_Z4PnjSLbs9bKKD2aTN2R5Ti8lcGK36nk'
how_to_do_great_work =  get_src_id_pdf_file(file_name="how to do great work",
                            file_path='/Users/spinokiem/Documents/Spino_DS_prj/privateGPT/source_documents/How to Do Great Work.pdf',
                            api_key=api_key
                            )
how_to_do_great_work

src_id = {"sac_xuat_thong_ke": 'src_iBTlKbIglvI8xwJ70t8oc', 
          "llama2_paper": "src_Arsacx2vZLICB1FH9f2lF",
          }

# 'https://scontent.fsgn5-2.fna.fbcdn.net/v/t39.2365-6/10000000_662098952474184_2584067087619170692_n.pdf?_nc_cat=105&ccb=1-7&_nc_sid=3c67a6&_nc_ohc=RYfzDCymkuYAX8KuQoc&_nc_ht=scontent.fsgn5-2.fna&oh=00_AfAYP0c7eCm5gg7HdKFZijWc4QZeN4HO9DHBInZ1yvniCg&oe=64C25B7F'
# ------------------------UPLOAD VIA FILES------------------------

# chatting with the pdf
def ask_pdf(question, sourceID):
    data = {
        'referenceSources': True, 
        # 'stream': True,
        'sourceId': sourceID,
        'messages': [
            {
                'role': "user",
                'content': question,
            }
        ]
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    if response.status_code == 200:
        # print('Result:', response.json()['references'])
        # print('Result:', response.json()['content'])
        print('success')
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
    return response.json()['content']
        
sourceID = 'src_iBTlKbIglvI8xwJ70t8oc'
# ask_pdf("Mode là gì? nó được trình bày trong chương nào?")
# ask_pdf("Mode là gì? Khái niệm này được trình bày trong chương mấy?")
response = ask_pdf("Cuốn sách này có mấy chương? kể tên các chương ấy, trả lời theo gạch đầu dòng", sourceID=sourceID)
print(response['content'])