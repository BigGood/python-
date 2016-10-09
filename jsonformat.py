class someutil:
    def toJson(self,obj,strObj):
        if type(obj)==list:
            strObj+="["
            for listV in obj:
                if type(listV)==dict or type(listV)==list:
                    strObj+=self.toJson(listV, "")
                    strObj+=","
                else:
                    strObj+=listV
                    strObj+=","
            strObj+="]"            
        if type(obj)==dict:
            strObj+="{"    
            for key in obj.keys():
                if type(obj[key])==dict or type(obj[key])==list:
                    strObj+="\""+key+"\""+":"
                    strObj+=self.toJson(obj[key], "")
                    strObj+=","
                else:
                    if type(key)==str:
                        strObj+="\""+key+"\""
                        strObj+=":"
                    if type(obj[key])==str:
                        strObj+="\""+obj[key]+"\""
                    else:
                        strObj+=str(obj[key]) 
                    strObj+=","        
            
            strObj+="}"             
        return strObj.replace(",}","}").replace(",]","]")


