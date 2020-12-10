import json
from unidecode import unidecode
import codecs

def make_file_name_map():
    start=0
    end=203
    list_filename=[]
    for i in range(start,end+1):
        strng="data/pythonnew"+str(i)+".json"
        list_filename.append(strng)
    return list_filename

list_filename=make_file_name_map()
def writetofile():
    for file in list_filename:
        outfilename="mod"+file
        fw=open(outfilename,'w')
        lines = [line.rstrip('\n') for line in codecs.open(file,"r",encoding='utf-8')]
        #print(lines[0]+"\n\n\n")
        print("Reading file: ",file)
        k=0
        for line in lines:
            line=line.encode("utf-8", errors='ignore')
            d=json.loads(line)
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

            json.dump(doc, fw)
            fw.write("\n")
        fw.close()
writetofile()            
