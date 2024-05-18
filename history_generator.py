from xml_parse import get_category

import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

def import_from_wiki(categories: list):
    output=""
    for category in categories:
        import_category=str(get_category(category))
        output+=import_category
    return output
preprompt_list=["Syndicate History","Syndicate Organizations","Races","Dungeon Mechanics"]
#["Syndicate History","Syndicate Organizations","Races","Dungeon Mechanics"]


preprompt=import_from_wiki(preprompt_list)
# with open('./data/preprompt_summarized.txt','r',encoding="utf-8") as file:
#     preprompt=file.read()
tokens=len(enc.encode(preprompt))
print(f"cost for gpt-4-turbo=${tokens*10/1e6:.2f}")
with open ('./data/preprompt.txt','w') as f:
    f.write(preprompt)