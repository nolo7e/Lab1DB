#! C:/Users/ivano/AppData/Local/Programs/Python/Python38-32/python.exe
print("Content-Type: text/html\n")
with open('head.inc') as file:
    for line in file:
        print(line.rstrip())

print('<table class=\'tView1\'>')

import mysql.connector
myconn = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '', db = 'electricbank', charset='utf8', use_unicode = True)
cur = myconn.cursor()
cur.execute("SET NAMES utf8;")
cur.execute("USE electricbank;")



# обновление, удаление строки в БД
import os
query_string = os.environ['QUERY_STRING']
if query_string is not None:
    import urllib.parse
    urlGets = urllib.parse.parse_qs(query_string)
    if 'delid' in urlGets:
        delid=str(urlGets['delid']).replace('[\'','').replace('\']','')
        cur.execute("DELETE FROM individuals WHERE id = "+delid)
        myconn.commit()
    if 'textId' in urlGets and 'textEd1' in urlGets and 'textEd2' in urlGets and 'textEd3' in urlGets:
        textId=str(urlGets['textId']).replace('[\'','').replace('\']','')
        textEd1=str(urlGets['textEd1']).replace('[\'','').replace('\']','')
        textEd2=str(urlGets['textEd2']).replace('[\'','').replace('\']','')
        textEd3=str(urlGets['textEd3']).replace('[\'','').replace('\']','')
        cur.execute("UPDATE individuals SET firstName='"+textEd1+"', lastName='"+textEd2+"', middleName='"+textEd3+"' WHERE id = "+textId)    
        myconn.commit()  
# конец обновления, удаления строки из БД

try: 
    cur.execute("SELECT * FROM individuals")
    result = cur.fetchall()
    for line in result:
        print('<tr>')
        iR=0
        for cell in line:
            sCellNew = str(str(cell).strip().encode('utf-8'), 'cp1251')
            sNewView = '<td title="Edit"><a href="#" class="js-open-modal" data-modal="1" id=\"id'+str(iR)+'_' + str(line[0]).strip() + '">' + sCellNew + '</a></td>'
            print(sNewView);
            iR+=1
        sNewView = '<td class="cellDel" title="Delete"><a href="index.py?delid=' + str(line[0]).strip() + '"><img src="image/delete2.png"></a></td>'
        print(sNewView);
        print('</tr>');
except: 
    myconn.rollback() 
 
myconn.close() 

print('</table>')

with open('foot.inc') as file:
    for line in file:
        print(line.rstrip())