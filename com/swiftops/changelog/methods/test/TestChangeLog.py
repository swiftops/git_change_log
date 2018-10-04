'''
Created on 17-Apr-2018

@author: hsolanki
'''
from unittest import TestCase
import services
import configparser

config1 = configparser.ConfigParser()
config1.read("com\\swiftops\\changelog\\methods\\test\\basedata.ini")

class TestGitChangeLog(TestCase):
    ## testcase for getproductshortstat api
    def test_getproductshortstat(self):
        actual=services.getproductshortstat("swiftalm_jboss6","4.0.0_0..4.0.0_1")
        expected = "{\"success\": \"true\", \"data\": {\"product\": true, \"customer\": \"\", \"filechnages\": \"59\", \"LOCinsertion\": \"1812\", \"LOCdeletion\": \"292\"}, \"error\": {}}"  
        self.assertEqual(actual, expected, "actual output doesnt match expected output") 
        
    ## testcase for getcustomshortstat  
    def test_getcustomshortstat(self):
        actual=services.getcustomshortstat("subex", "swiftalm_jboss6", "subex_3.2.1_IR1..subex_3.2.1_IR2")    
        expected = "{\"success\": \"true\", \"data\": {\"product\": false, \"customer\": \"subex\", \"filechnages\": \"3\", \"LOCinsertion\": \"17\", \"LOCdeletion\": \"1\"}, \"error\": {}}"
        self.assertEqual(actual, expected, "actual ouput doesnt match expected output")       
     
    ## test case for   getproductshortstat api with invalid repo name   
    def test_getproductshortstat_invalid_repo(self):
        actual=services.getproductshortstat("swiftalm_jbos","4.0.0_0..4.0.0_1")
        expected = "{\"success\": \"false\", \"data\": {}, \"error\": {\"product\": true, \"customer\": \"\", \"statuscode\": 400, \"errormsg\": \"exception occured while fetching repo from git. Exception is [WinError 267] The directory name is invalid\"}}"  
        self.assertEqual(actual, expected, "actual output doesnt match expected output")         
      
    ## test case for getproductchangedfiles
    def test_getproductchangedfiles(self): 
        actual=services.getproductchangedfiles("swiftalm_jboss6","4.0.0_0..4.0.0_1")
        expected = config1.get("DATA", "expected")
        self.assertEqual(actual, expected, "actual output doesnt match expected output")
      
    ## test case for getproductchangedfiles with ivalid repo name       
    def test_getproductchangedfiles_invalid_repo(self): 
        actual=services.getproductchangedfiles("swiftalm_jboss","4.0.0_0..4.0.0_1")
        expected = "{\"success\": \"false\", \"data\": {}, \"error\": {\"product\": true, \"customer\": \"\", \"statuscode\": 400, \"errormsg\": \"exception occured while fetching repo from git. Exception is [WinError 267] The directory name is invalid\"}}"
        self.assertEqual(actual, expected, "actual output doesnt match expected output")

    ## testcase for getcustomchangedfiles   api
    def test_getcustomchangedfiles(self):
        actual=services.getcustomchangedfiles("subex", "swiftalm_jboss6", "subex_3.2.1_IR1..subex_3.2.1_IR2")    
        expected="{\"success\": \"true\", \"data\": {\"product\": false, \"customer\": \"subex\", \"database/subex/mssql/dml/DML.SQL\": \"Modified\", \"sourcecode/com/subex/swift/adaptor/SubexFTPDownloader.java\": \"Modified\", \"sourcecode/com/subex/swift/util/SubexConstants.java\": \"Modified\"}, \"error\": {}}"
        self.assertEqual(actual, expected, "actual ouput doesnt match expected output")       
             