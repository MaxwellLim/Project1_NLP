import pickle, re, xml.etree.ElementTree as ET
from os.path import exists

def chatbot(knowledge_base):
    profile_root = ""
    name = input(knowledge_base['greeting'])
    if exists(f"{name}.xml"):
        profile_tree = ET.parse(f"{name}.xml")
        profile_root = profile_tree.getroot()
    else:
        profile_root = ET.Element('Profile')
        profile_name =  ET.SubElement(profile_root, "Name")
        profile_name.text = name

    


def makecorpora():
    corpora = {
        'greeting': "Hello, I am a chatbot designed to tell you about CaptainSparklez AKA Jordan Maron.\nWhat is your name?",
        'base' : "What would you like to know about Captainsparklez?",
        'reset' : "(To end session type \"Finished\")",
        'creeper' : "A creeper is a hostile mob in the video game Minecraft",
        'residence' : "He lives in Los Angeles",
        'polaris' : "Polaris is a Multi-channel Network which was started in 2009 and is now defunct",
        'bethesda' : "They are a large video game publisher which has published many popular games such as the Fallout and Elder Scroll series along with many others",
        'telltale' : "The company which made Minecraft: Story mode",
        'minecraft: story mode' : "Minecraft: Story Mode is a point and click adventure game based on Minecraft and features many popular Minecraft Youtubers",
        'tnt' : "Tnt is a minecraft parody of the popular song by Taio Cruz: \"Dynamite\"",
        'minecraft' : "Minecraft is a popular survival game where you can mine blocks and craft items in order to survive",
        'fortress fury' : "A mobile game which was created by CaptainSparklez in collaboration with Howard Marks under XREAL. It was originally titled \"Fortress Fallout\" but was renamed due to intervention by Bethesda",
        'notch' : "Notch AKA Markus Persson is a Swedish video game programmer who is best known for creating the popular bideo game \"Minecraft\"",
        'infringement' : "Bethesda sent a cease and desist letter to XREAL to get them to change the name of their game from \"Fortress Fallout\" to something else as they feared people might mistake it with their upcoming game \"Fallout Shelter\""
    }
    pickle.dump(corpora, open('knowledge_base.p', 'wb'))

def main():
    makecorpora()
    chatbot(pickle.load(open('knowledge_base.p', 'rb')))
    

if __name__ == '__main__':
    main()