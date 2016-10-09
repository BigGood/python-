import re
import os
# os.chdir('G://newWorkspace/zsw_web/WebRoot/jsp');
# print(os.listdir());
# file_w = open('C://Users/Administrator/Desktop/htmlLanguage.txt',"w")
# for name in os.listdir():
#     file_w.write("\n")
#     file_w.write("\n")
#     file_w.write("\n")
#     file_w.write("\n")
#     print(name)
#     file_w.write(name+"\n");
#     if not (os.path.isdir('G://newWorkspace/zsw_web/WebRoot/jsp/'+name)):
#         print(name[-5:])
#         if name[-5:]==".html":
#             file_object = open('G://newWorkspace/zsw_web/WebRoot/jsp/'+name,encoding="utf-8")
#             try:
#                  all_the_text = file_object.readlines()
#                  for EachLine in all_the_text:
#                      str = re.findall( r"[\u4e00-\u9fa5]+",EachLine)
#                      if str:
#                          print(str)
#                          if type(str)==list:
#                              for go in str:
#                                  file_w.write(go+"\n")
#                          else:        
#                              file_w.write(str+"\n")
#             finally:
#                  file_object.close()
# file_w.close()    
dataFile = open('C://Users/Administrator/Desktop/zhongwen.txt',encoding="utf-8")
data={} 
try:
    all_the_text = dataFile.readlines()
    for EachLine in all_the_text:
        str = EachLine.split("=");
        if len(str)>1:
            data[str[1]]=str[0]
finally:
    dataFile.close()
         
         
os.chdir('G://newWorkspace/zsw_web/WebRoot/jsp');
for name in os.listdir():
    if not (os.path.isdir('G://newWorkspace/zsw_web/WebRoot/jsp/'+name)):
        if name[-4:]==".jsp":              
            file_object = open('G://newWorkspace/zsw_web/WebRoot/jsp/'+name,"r",encoding="utf-8")
            file_object1 = open('C://Users/Administrator/Desktop/newjsp2/'+name,"w",encoding="utf-8")
            try:
                all_the_text = file_object.readlines()
                for EachLine in all_the_text:
                    str = re.findall( r"[\u4e00-\u9fa5]+",EachLine)
                    if str:
                        print(str)
                        if type(str)==list:                              
                            for go in str:
                                if data.get(go+"\n"):
                                    EachLine = EachLine.replace(go,'<%=rb.getString(\"'+data[go+"\n"]+'\") %>')
                            file_object1.write(EachLine)                 
                        else: 
                            if data.get(str+"\n"):       
                                file_object1.write(EachLine.replace(str,'<%=rb.getString(\"'+data[str+"\n"]+'\") %>'))  
                    else:
                        file_object1.write(EachLine);            
            finally:
                file_object1.close()        

