import pymongo
import os

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "myTestDB"
COLLECTION_NAME = "myFirstMDB"


def mongo_connect(url):
    
    """ Create the connection string """
    
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e
        

def show_menu():
    
    """ Custom User Interface Function """
    
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")
    
    option = input("Enter Option: ")
    return option
    
    
def get_record():
    
    """ Create a little helper function, which is going to assist us with our find, edit, and delete functions later on """
    
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")

    try:
        doc = coll.find_one({'first': first.lower(), 'last': last.lower()})
    except:
        print("Error accessing the database")
    
    if not doc:
        print("")
        print("Error! No results found.")
    
    return doc
    
    
def add_record():
    print("")
    first = input("Enter First Name > ")
    last = input("Enter Last Name > ")
    dob = input("Enter Date of Birth > ")
    gender = input("Enter Gender > ")
    hair_colour = input("Enter Hair Colour > ")
    occupation = input("Enter Occupation > ")
    nationality = input("Enter Nationality > ")
    
    # Create a new variable called new_doc and we'll start building the dictionary
    new_doc = {'first': first.lower(), 'last': last.lower(), 'dob': dob,
               'gender': gender, 'hair_colour': hair_colour, 'occupation':
               occupation, 'nationality': nationality}
               
    try:
        coll.insert(new_doc)
        print("")
        print("Document Inserted!")
    except:
        print("Error accessing the database")
        
        
def find_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())
                
                
def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        for k, v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")
                
                # If we haven't actually entered anything for update_doc, if we've just left it blank, we don't actually want to delete the information that's in there. We just want to leave it the same as it was before. We're going to set update_doc[k] back to the value of v.
                if update_doc[k] == "":
                    update_doc[k] = v
        
        try:
            coll.update_one(doc, {'$set': update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing the database")

            
            
def delete_record():
    doc = get_record()
    
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())
                
        print("")
        confirmation = input("Is this the document you want to delete?\nY or N > ")
        print("")
        
        if confirmation.lower() == "y":
            try:
                coll.remove(doc)
                print("Document Deleted!")
            except:
                print("Error accessing the database")
        else:
            print("Document not deleted!")

def main_loop():
    
    """ So now that we've done that, we need to define our main loop.
    So this will continue to call the menu every time we come back to it"""
    
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            # Add a break, which exits from the program.
            break
        else:
            print("Invalid Option")
        print("")
        
        
""" Create the connection object from Mongo, go back to the previous project, mongo.py file """

conn = mongo_connect(MONGODB_URI)
coll = conn[DBS_NAME][COLLECTION_NAME]

main_loop()
