import pickle, re, spacy ,xml.etree.ElementTree as ET, random, os
from nltk.corpus import wordnet as wn

def get_profile(name):
    path = f"./profiles/{name}.xml"
    
    if os.path.exists(path):
        tree = ET.parse(path)
        root = tree.getroot()
        visit = root.find('Visits')
        visit.text = str(int(visit.text) + 1)
    else:
        root = ET.Element('Profile')
        profile_name =  ET.SubElement(root, "Name")
        visits = ET.SubElement(root, "Visits")
        visits.text = "1" 
        profile_name.text = name
        tree = ET.ElementTree(root)
    return tree

def chatbot(knowledge_base):
    
    name = input(knowledge_base['greeting'])
    tree = get_profile(name)
    print(f"Welcome {name},")
    query = input(knowledge_base['base']).lower()
    while True:
        if query == "finished":
            print("Thank you for chatting with me")
            break
        
        if re.match(".*summary.*", query):
            print(knowledge_base['overview'])
        elif re.match(".*game.*", query):
            if re.match(".*play.*", query):
                print(knowledge_base['games_played'])
                query = input("Which one would you like to know more about?").lower()
                if re.match(".*minecraft.*", query):
                    if re.match(".*story.*", query):
                        print(knowledge_base['minecraft: story mode'])
                        input(knowledge_base['more']).lower()
                        if re.match(".*telltale.*", query):
                            print(knowledge_base['telltale'])
                    else:
                        print(knowledge_base['minecraft'])
            if re.match(".*made.*", query):
                print(knowledge_base['games_made'])
                input('Would you like to know more?').lower()
                if re.match(".*yes.*", query):
                    print(knowledge_base['fortress_fury'])
        else:
            print(knowledge_base['default'])
        print("(To end session type \"finished\")")
        query = input(knowledge_base['base']).lower()

    if not os.path.exists('./profiles'):
            os.makedirs('./profiles')
    tree.write(f"./profiles/{name}.xml")




def main():   
    chatbot(pickle.load(open('knowledge_base.p', 'rb')))
    

if __name__ == '__main__':
    main()