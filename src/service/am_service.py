import sys
from io import StringIO
from dao.milvus_helpers import MilvusHelper
from dao.mysql_helpers import MySQLHelper
from entity.am import AM
import pandas as pd
from config import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION, VECTOR_DIMENSION, METRIC_TYPE
from encode import SentenceModel


class amService():
    def __init__(self):
        # initialize persistence tool
        self.mysql_cli = MySQLHelper()
        self.milvus_cli = MilvusHelper()
        self.encoder = SentenceModel()
        # build basic table、collection
        self.milvus_cli.create_collection()

    def toJsonList(self, data):
        res = [AM(item[0], item[1], item[2], item[3],
                  item[4], item[5], item[6], item[7]) for item in data]
        return res

    def get_newest_10_from_am(self):
        res = self.mysql_cli.get_newest_10_from_am()
        res = self.toJsonList(res)
        return res

    def get_am_by_company_name(self, company_name):
        res = self.mysql_cli.get_am_by_company_name(company_name)
        res = self.toJsonList(res)
        return res

    def recommend_by_description(self, description):
        v = self.encoder.sentence_encode(description)
        res = self.milvus_cli.search_vectors(v, 30)
        res = list(zip(res[0].distances, res[0].ids))
        res.sort(key=lambda x: x[0], reverse=True)
        mids = [(x[1]) for x in res]
        res = self.mysql_cli.search_am_by_mids(mids)
        res = self.toJsonList(res)
        return res

    def recommend_by_company_id(self, company_id):
        # get the current company's mid
        curr_mid = self.mysql_cli.get_mid_by_company_id(company_id)[0][0]
        # get the current company's capabilities code
        curr_capCode = self.mysql_cli.get_cap_code_by_company_id(company_id)
        # get the most similar (with this company description) top 30 vector's mid 
        vectors = self.milvus_cli.search_vectors_by_mid(curr_mid, 30)
        res = list(zip(vectors[0].distances, vectors[0].ids))
        res.sort(key=lambda x: x[0], reverse=True)
        mids = [(x[1]) for x in res]
        sql_like_addition = ' OR '.join(
            ['capability_am.CapCode like \'%'+str(x[0])+'\' ' for x in curr_capCode])
        res = self.mysql_cli.get_am_by_mid_and_cap_code(
            mids, sql_like_addition)
        res = self.toJsonList(res)
        return res

    def get_all_capability(self):
        cap = self.mysql_cli.get_all_capability()
        res = [{'label': x[0], 'value':x[1]} for x in cap]
        print(cap)
        return res

    def import_am_data(self, content_str):
        # create collection if it doesn't exist
        # connect milvus database
        self.milvus_cli.create_collection()  
        self.milvus_cli.set_collection()
        # read the import data
        with StringIO(content_str) as file:
            csv = pd.read_csv(file)
            # traverse all the data
            for index, row in csv.iterrows():
                # do embedding to the text, get feature vector
                v = self.encoder.sentence_encode(
                    row['CompanyName']+" "+row['CompanyDescription'])
                # let the vector import milvus, get mid
                mid = self.milvus_cli.insert(v)
                # let am import mysql
                self.mysql_cli.insert_new_am(row['CompanyID'], row['CompanyName'], row['WebSite'],
                                             row['CompanyDescription'].replace("\'", "\\\'").replace(
                                                 "\"", "\\\""), row['DefaultAddress'], row['Interests'],
                                             row['Products'], row['Projects'], mid[0])
                # let am's capability import mysql
                caps_str = row['Capabilities'][1:-1]
                caps = caps_str.split(',')
                temp = [(row['CompanyID'], item) for item in caps]
                self.mysql_cli.insert_capabilities_am(temp)
        return {'success': True}

    def insert_am_and_capabilities(self, name, website, address,
                                   interest, product, project, description, capability):
        description = description.replace("\'", "\\\'").replace("\"", "\\\"")
        companyId = self.mysql_cli.insert_new_am_2(name, website, description, address,
                                                 interest, product, project)
        caps = capability.split(",")
        temp = [(companyId, item) for item in caps]
        self.mysql_cli.insert_capabilities_am(temp)
        return companyId