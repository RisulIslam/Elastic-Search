import json
from unidecode import unidecode
import codecs

from elasticsearch import Elasticsearch
es=Elasticsearch()

import geocoder
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import os

def getmyloc():
    g = geocoder.ip('me')
    #print(g.latlng) # list with two element 0==latitude 1== longitude
    return g.latlng

myloc=getmyloc()

#my_map1.add_child(folium.ClickForMarker(popup='Current Location'))




def make_file_name_map():
    start=0
    end=203
    list_filename=[]
    for i in range(start,end+1):
        strng="moddata/pythonnew"+str(i)+".json"
        list_filename.append(strng)
    return list_filename

#list_filename=make_file_name_map()

def construct_index():
    for file in list_filename:
        lines = [line.rstrip('\n') for line in codecs.open(file,"r",encoding='utf-8')]
        #print(lines[0]+"\n\n\n")
        print("Reading file: ",file)
        k=0
        for line in lines:
            line=line.encode("utf-8", errors='ignore')
            k+=1
            if k%100==0:
                #break
                print("line: ",k)
            doc=json.loads(line)
            """
            map={}
                
            map['created_at']=d['created_at']
            map['id']=d['id']
            if d['text']!=None:
                map['text']=unidecode(d['text'])
            else:
                map['text']=unidecode("Default")
            
            if d['user']['name']!=None:
                map['username']=unidecode(d['user']['name'])
                #map['username']=map['username'].encode("utf-8", errors='ignore')
            else:
                map['username']=unidecode("Default")
            if d['user']['screen_name']!=None:
                map['screenname']=unidecode(d['user']['screen_name'])
            else:
                map['screenname']=unidecode("Default")
            
            if d['user']['location']!=None:
                map['location']=unidecode(d['user']['location'])
            else:
                map['location']=unidecode("Riverside")
            jsn_str = json.dumps(map)
            
            doc = json.loads(jsn_str)
            #print(doc)
            """
            es.index(index="english",doc_type="sentences",id=doc['id'],body=doc)
        #break
#construct_index()

def construct_map(address,myloc,radius,name,my_map1):
    
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    try:
        location = geolocator.geocode(address)
    except:
        location=None
    if location==None:
        print(address," coordinate can not be found in map")
    else:
        full_address=location.address
        tweetcoordinate=[location.latitude,location.longitude]
        #print(full_address)
        #print(tweetcoordinate)

        newport_ri = (myloc[0], myloc[1])
        cleveland_oh = (tweetcoordinate[0], tweetcoordinate[1])
        distance_in_mile=geodesic(newport_ri, cleveland_oh).miles
        pup="Location:"+address+"  User:"+name
        print("Distance from this user to ",pup, ": ",distance_in_mile)
        

        if distance_in_mile<=radius:
            # CircleMarker with radius 
            folium.Marker(location = tweetcoordinate, 
                                popup = pup).add_to(my_map1)
            #my_map1.add_child(folium.ClickForMarker(popup=address))
    return my_map1
    




def queryres(query,query_field,number_of_result,radius,my_map1):
    query_format={"from":0,"size":2,"query":{"match":{query_field:query}},"terminate_after":number_of_result}
    res= es.search(index="english",body=query_format)
    #print(res['hits']['hits'][0]['_source'])
    total_hits=res['hits']['total']
    print("Total hits: ",total_hits)
    if total_hits>=1:
        query_format={"from":0,"size":total_hits,"query":{"match":{query_field:query}}}
        res= es.search(index="english",body=query_format)
        map_loc_name={}
        for j in range(0,total_hits):
            output=res['hits']['hits'][j]['_source']
            if 'username' in output and 'created_at' in output and 'location' in output and 'text' in output and 'id' in output:
                name=unidecode(output['username'])
                ct=unidecode(output['created_at'])
                loc=unidecode(output['location'])
                print(ct,"    ",name,"  ",loc)
                map_loc_name[loc]=name

        print("\n\nConstructing map. Please wait....")        
        for lctn in map_loc_name.keys():
            my_map1=construct_map(lctn,myloc,radius,map_loc_name[lctn],my_map1)
        print("Map construction finished. Reload the Map.")
        my_map1.save("my_map1.html")
    else:
        my_map1.save("my_map1.html")
        
    
    #print(res)
        
        


def arrange_query(query,indexing_type,number_of_result,radius,my_map1):
    
    number_of_result=int(number_of_result/5)
    queryres(query,indexing_type,number_of_result,radius,my_map1)

    
from tkinter import *
from tkinterhtml import HtmlFrame
import webbrowser


    
class Windowmap(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        
        w = Label(self, text="Search Based on Location/Text")
        w.pack()
        
        self.var1 = StringVar(self)
        # initial value
        self.var1.set('location')
        choices = ['location', 'text']
        option = OptionMenu(self, self.var1, *choices)
        option.pack(side='top', padx=10, pady=10)

        w = Label(self, text="Number of Search Result")
        w.pack()
        
        self.var2 = StringVar(self)
        # initial value
        self.var2.set(20)
        choices = [20, 50, 100, 250,500, 1000]
        option = OptionMenu(self, self.var2, *choices)
        option.pack(side='top', padx=10, pady=10)

        w = Label(self, text="Radius in Google Map")
        w.pack()

        self.var3 = StringVar(self)
        # initial value
        self.var3.set(50)
        choices = [50, 100, 150, 200,500, 1000]
        option = OptionMenu(self, self.var3, *choices)
        option.pack(side='top', padx=10, pady=10)

        w = Label(self, text="Enter the Query")
        w.pack()
        
        self.textBox=Text(self, height=2, width=10)
        self.textBox.pack()

        w = Label(self, text="Click the button below and See the result in the console while map is being processed. You will see the map in your browser.")
        w.pack()

        # creating a button instance
        quitButton = Button(self, text="Show Result",command=self.quitbuttoneventhandler)

        # placing the button on my window
        #quitButton.place(x=300, y=300)
        quitButton.pack()
    def quitbuttoneventhandler(self):
        #print("Quit button clicked")
        #printline()
        print(self.var1.get())
        print(self.var2.get())
        print(self.var3.get())

        inputquery=self.textBox.get("1.0","end-1c")
        print(inputquery)

        
        my_map1 = folium.Map(location = myloc,zoom_start = 7)
        folium.CircleMarker(location = myloc, color='red', 
                                radius = 15, popup = 'Current Location').add_to(my_map1)
        arrange_query(inputquery,self.var1.get(),int(self.var2.get()),int(self.var3.get()),my_map1)


        #url = 'file://C:/Users/Risul Islam/Desktop/python testing codes/elastic search/my_map1.html'
        webbrowser.open('file://' + os.path.realpath("my_map1.html"),new=2)
        w = Label(self, text="Set up the Query and click the button again.")
        w.pack()
        #webbrowser.open(url, new=2)  # open in new tab
        #frame = HtmlFrame(self, horizontal_scrollbar="auto")
        #frame.set_content(my_map1.html)
        """
        bw=Tk()
        bw.geometry("400x400")
        q = Windowmap(bw)
        bw.mainloop()
        """

        
        
        

root = Tk()

#size of the window
root.geometry("400x400")

app = Window(root)
root.mainloop()

    
        
"""
doc1={"sentence": "today is sunny","name":"raisul","location": "Riverside"}
doc2={"sentence": "today bright-sunny","name":"Raisul","location": "San diego"}


es.index(index="english",doc_type="sentences",id=1,body=doc1)
es.index(index="english",doc_type="sentences",id=2,body=doc2)

query="sunny"
query_format={"from":0,"size":2,"query":{"match":{"sentence":query}}}


res= es.search(index="english",body=query_format)
print(res['hits']['hits'][0]['_source'])
"""
