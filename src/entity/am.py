import json

class AM():
    def __init__(self,CompanyID,CompanyName,WebSite,CompanyDescription,\
        DefaultAddress,Interests,Products,Projects):
        self.CompanyID =CompanyID
        self.CompanyName =CompanyName
        self.WebSite =WebSite
        self.CompanyDescription =CompanyDescription
        self.DefaultAddress =DefaultAddress
        self.Interests =Interests
        self.Products =Products
        self.Projects =Projects
    
    def getJson(self):
        res=json.dumps(self.__dict__)
        return res
    
