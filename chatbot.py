import pickle, re, xml.etree.ElementTree as ET, random, os
random.seed(42)

#create or open an xml file with the users name
def get_profile(name):
    path = f"./profiles/{name}.xml"
    
    #check if it exists and update visit count
    if os.path.exists(path):
        tree = ET.parse(path)
        root = tree.getroot()
        visit = root.find('Visits')
        visit.text = str(int(visit.text) + 1)

    #create it if it doesnt exist
    else:
        root = ET.Element('Profile')
        profile_name =  ET.SubElement(root, "Name")
        visits = ET.SubElement(root, "Visits")
        visits.text = "1" 
        profile_name.text = name
        tree = ET.ElementTree(root)
    return tree, root

#return a rating making sure the input is a number between 1 and 10
def get_rating(output):
    while True:
        response = input(output)
        if response.isnumeric():
            if int(response)>0 and int(response) < 11:
                return response
        print("Response must be a number between 1 and 10.")
    

#convert numeral into ordinal form
def num_to_ordinal(num):
    last_digit = num[len(num)-1]
    if last_digit == '1':
        num += 'st'
    elif last_digit == '2':
        num += 'nd'
    elif last_digit == '3':
        num += 'rd'
    else:
        num += 'th'
    return num

#create ratings for the chatbot and store them under the xml file
def rating(root):
    rating = ET.SubElement(root, "Ratings")
    accuracy = ET.SubElement(rating, "Accuracy")
    detail = ET.SubElement(rating, "Detail")
    recommend = ET.SubElement(rating, "Recommended")
    overall = ET.SubElement(rating, "Overall")

    print("On a scale from 1 to 10 answer the following questions")
    accuracy.text = get_rating("How accurate were the responses based on your queries? ")
    detail.text = get_rating("What was your satisfaction with the amount of detail provided by the answers? ")
    recommend.text = get_rating("How likely are you to recommend this chatbot to a friend? ")
    overall.text = get_rating("How would you rate your overall experience with the chatbot? ")
    return int(overall.text)

#code for rules based chatbot using regex to parse queries
def chatbot(k_base):
    #greet user and ask for name
    name = input(k_base['greeting'][random.randint(0,1)])

    #create or retrieve user profile for name
    tree, root= get_profile(name)
    num_visits = num_to_ordinal(tree.find('Visits').text)
    
    #welcome user
    print(f"Welcome {name}, this is your {num_visits} visit. ")
    query = input(f"{k_base['base']}(I can give you a summary if you are unsure of what to ask about.)\n").lower()
    
    #Dialog loop
    while True:
        if re.match(".*finished.*", query):
            break
        
        if re.match(".*summary.*", query):
            print(k_base['overview'])

        elif re.match(".*live.*", query):
            print(k_base['residence'])

        elif re.match(".*song.*", query):
            print(k_base['songs'])
            query = input(k_base['more']).lower()
            if re.match(".*tnt.*", query):
                print(k_base['tnt'])
            else:
                print(k_base['default'])
        
        elif re.match(".*partner.*", query):
            print(k_base['partner'])
            query = input(k_base['more']).lower()

            if re.match(".*polaris.*", query):
                print(k_base['polaris'])
            elif re.match(".*pocketwatch.*", query):
                print(k_base['pocketwatch'])
            else:
                print(k_base['default'])

        elif re.match(".*game.*", query):

            if re.match(".*play.*", query):
                print(k_base['games_played'])
                query = input(k_base['more']).lower()

                if re.match(".*minecraft.*", query):
                    minecraft = True
                    if re.match(".*story.*", query):
                        minecraft=False
                        print(k_base['minecraft: story mode'])
                        query = input(k_base['more']).lower()
                        if re.match(".*telltale.*", query):
                            print(k_base['telltale'])
                        elif re.match(".*minecraft.*", query):
                            minecraft = True
                        else:
                            print(k_base['default'])
                    if minecraft:
                        print(k_base['minecraft'])
                        query = input(k_base['more']).lower()
                        if re.match(".*creeper.*", query):
                            print(k_base['creeper'])
                        if re.match(".*notch.*", query):
                            print(k_base['notch'])
                        else:
                            print(k_base['default'])
                else:
                    print(k_base['default'])

            elif re.match(".*made.*", query):
                print(k_base['games_made'])
                query = input('Would you like to know more?').lower()
                if re.match(".*yes.*", query):
                    print(k_base['fortress_fury'])
                    query = input(k_base['more']).lower()
                    if re.match(".*infringement.*", query):
                        print(k_base['infingement'])
                    if re.match(".*bethesda.*", query):
                        print(k_base['bethesda'])
            else:
                print(k_base['default'])
        else:
            print(k_base['default'])
        print("(To end session type \"finished\")")
        query = input(k_base['base']).lower()

    #get ratings on the chat bot
    overall = rating(root)
    if overall>5:
        print("Thank you for chatting with me. I enjoyed our conversation.")
    else:
        print("Thank you for chatting with me. I hope your next time is more enjoyable.")
    
    #save the user profile to a file
    if not os.path.exists('./profiles'):
            os.makedirs('./profiles')
    tree.write(f"./profiles/{name}.xml")

#run chatbot with the knowledge base
def main():   
    chatbot(pickle.load(open('knowledge_base.p', 'rb')))
    

if __name__ == '__main__':
    main()