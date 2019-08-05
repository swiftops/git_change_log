from subprocess import check_output
import configparser
import os
import json

config = configparser.ConfigParser()
config.read("com/swiftops/changelog/methods/gitconfig.ini")


def getcustomervswebuijson():
    """
    This api will return webui\cobrand folder name for customer.
    :return:
    """
    return getcustomervswebuijsonforcustomer(None)


def getcustomervswebuijsonforcustomer(customer):
    """git@gitserver.digite.in:devops-MS/MS-GitChangeLog.git
    This will return json, customername as key and webui folder name as value.
    :return:
    """

    errordata = {}
    try:
        customer_webui = str(config.get("DEFAULT", "customer_webui")).split(",")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    customer_webui_json = {}

    for item in customer_webui:
        customer_webui_json[item.split("#")[0]] = item.split("#")[1]

    if(customer == None):
        return customer_webui_json
    else:
        return customer_webui_json.get(customer)


def validatecustomer(customer):
    """
    Validate customer name exists OR not
    :param customer:
    :return:
    """

    # validate customer name. Valid customer OR not.
    try:
        customlist = str(config.get("DEFAULT", "customers")).split(",")
        if not customlist.__contains__(customer):
            raise Exception('Customer not found. Customer name should be from' + customlist.__str__())
    except Exception:
        return False
    return True


def getfilterpathforcustomer(customer, gitrepo, workspace):
    """
    This api will fetch filter to filter git log based on customer name.
    :param customer:
    :return:
    """
    errordata = {}
    if not validatecustomer(customer):
        errordata["statuscode"] = 404
        errordata["errormsg"] = "Exception occured while validating customer."
        return builderrorresponse(errordata)

    try:
        included_paths = str(config.get("GITINCLUSION", "customer")).split(",")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    customervswebui = getcustomervswebuijsonforcustomer(customer)
    returnval = []
    for path in included_paths:
        temp = path
        temp = temp.replace("#customer#", customer)
        temp = temp.replace("#customer_webui#", customervswebui)
        if os.path.exists(workspace + os.sep + gitrepo + os.sep + temp):
            returnval.append(temp)

    return returnval


def getproductshortstat(gitrepo, tags):
    """
    This api will return git short stat from given tags only for product sourcecode mentioned in gitconfig.ini for section GITINCLUSION and property product.
    :param gitrepo: salm_core OR salm_automation
    :param tags: 3.2.0_12..3.2.0_13
    :return:
    """
    errordata = {}

    try:
        workspace = config.get("GITCHANGELOG", "workspace_dir")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        included_paths = str(config.get("GITINCLUSION", "product")).split(",")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    return getshortstat(gitrepo, tags, included_paths, None, workspace)


def getcustomshortstat(gitrepo, tags, customer):
    """
    This api will return git short stat for given tags only for custom sourcecode.
    This custom mapping mentioned in gitconfig.ini for section GITINCLUSION and property custom.
    :param gitrepo:
    :param tags:
    :param customer:
    :return:
    """
    errordata = {}

    try:
        workspace = config.get("GITCHANGELOG", "workspace_dir")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    return getshortstat(gitrepo, tags, getfilterpathforcustomer(customer, gitrepo, workspace), customer, workspace)


def getshortstat(gitrepo, tags, includepath, customer, workspace):
    """
    This will return git shortstats for tags passed to methods
    :param gitrepo:
    :param tags:
    :param includepath:
    :param customer:
    :return:
    """
    jsondata = {}
    errordata = {}

    #Put customer info in return json
    if(customer == None):
        jsondata["product"] = True
        jsondata["customer"] = ""
        errordata["product"] = True
        errordata["customer"] = ""
    else:
        jsondata["product"] = False
        jsondata["customer"] = customer
        errordata["product"] = False
        errordata["customer"] = customer

    srcpath = workspace + os.path.sep + gitrepo

    try:
        check_output(["git", "fetch"], cwd=srcpath)
    except Exception as e:
        errordata["statuscode"] = 400
        errordata["errormsg"] = "exception occured while fetching repo from git. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        shortstats = check_output(["git", "diff", tags, "--shortstat"] + includepath, cwd=srcpath)
        shortstats = str(shortstats)
    except Exception as e:
        errordata["errorcode"] = 400
        errordata[
            "errormsg"] = "exception occured while getting shortstat for " + tags + " for " + gitrepo + ". Exception is " + e.__str__()
        return builderrorresponse(errordata)

    commit_stats_values = []
    for each in shortstats[2:-3].split(","):
        if each.__len__() > 0:
            commit_stats_values.append(each.split(" ")[1])

    if commit_stats_values.__len__() > 0:
        jsondata["filechnages"] = commit_stats_values[0]
        jsondata["LOCinsertion"] = commit_stats_values[1]
        jsondata["LOCdeletion"] = commit_stats_values[2]
    else:
        jsondata["filechnages"] = 0
        jsondata["LOCinsertion"] = 0
        jsondata["LOCdeletion"] = 0

    return getsuccessresponse(jsondata)


def getproductchangedfiles(gitrepo, tags):
    """
    This api will return git changed files set for given tags only from product sourcecode mentioned in gitconfig.ini for section GITINCLUSION and property product.
    :param gitrepo:
    :param tags:
    :return:
    """
    errordata = {}

    try:
        workspace = config.get("GITCHANGELOG", "workspace_dir")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        included_paths = str(config.get("GITINCLUSION", "product")).split(",")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)
    return getchangedfiles(gitrepo, tags, included_paths, None, workspace)


def getcustomchangedfiles(gitrepo, tags, customer):
    """
    This api will return git changed files set for given tags only from custom sourcecode mentioned in gitconfig.ini for section GITINCLUSION and property customer.
    :param gitrepo:
    :param tags:
    :param customer:
    :return:
    """

    errordata = {}

    try:
        workspace = config.get("GITCHANGELOG", "workspace_dir")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    return getchangedfiles(gitrepo, tags, getfilterpathforcustomer(customer, gitrepo, workspace), customer, workspace)


def getchangedfiles(gitrepo, tags, includepath, customer, workspace):
    """
    This will return git shortstats for tags passed to methods
    :param gitrepo:
    :param tags:
    :param includepath:
    :return:
    """
    jsondata = {}
    errordata = {}

    # Put customer info in return json
    if customer is None:
        jsondata["product"] = True
        jsondata["customer"] = ""
        jsondata["tabulardata"] = [["File Name","Status"]]
        errordata["product"] = True
        errordata["customer"] = ""
    else:
        jsondata["product"] = False
        jsondata["customer"] = customer
        jsondata["tabulardata"] = [["File Name","Status"]]
        errordata["product"] = False
        errordata["customer"] = customer

    srcpath = workspace + os.path.sep + gitrepo

    try:
        check_output(["git", "fetch"], cwd=srcpath)
    except Exception as e:
        errordata["statuscode"] = 400
        errordata["errormsg"] = "exception occured while fetching repo from git. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        changedfiles = check_output(["git", "diff", tags, "--name-status"] + includepath, cwd=srcpath)
        changedfiles = str(changedfiles)
    except Exception as e:
        errordata["errorcode"] = 400
        errordata[
            "errormsg"] = "exception occured while getting name status for " + tags + " for " + gitrepo + ". Exception is " + e.__str__()
        return builderrorresponse(errordata)

    file_changed = []
    lines2 = str(changedfiles)[1:].split("\\n")
    for line in lines2:
        file_changed.append(line)

    # remove empty output from list
    if len(file_changed) != 1:
        file_changed.remove("'")

    # remove unwanted chr from list items.
    file_changed = [s.strip("'") for s in file_changed]
    list_files=[]
    # Change M, A, D, R shortform of file actions to Fulform such as Modified, Added, Deleted, Renamed/Moved.
    for item in sorted(file_changed):
        if len(item) < 2:
            break
        elif item[0] == "'":
            file_status = {'M': "Modified", 'A': "Added", 'D': "Deleted",'R':"Renamed/Moved"}.get(item[1], "none")
        else:
            file_status = {'M': "Modified", 'A': "Added", 'D': "Deleted",'R':"Renamed/Moved"}.get(item[0], "none")
        if item.count('\\t') == 2 and file_status == 'Renamed/Moved':
            #if file is moved or renamed
            file_name=item.split('\\t')[1]
            file_status='{} to {}'.format(file_status,item.split('\\t')[2])
        else:
            file_name = item[item.find('\\t') + 2:]
        list_files.append([file_name, file_status])

    jsondata["tabulardata"].append(list_files)
    return getsuccessresponse(jsondata)


def getdaywiseproductstats(gitrepo, fromdate, todate, branch, customer):
    """
    This api will return git changed files set for given tags only from product sourcecode mentioned in gitconfig.ini for section GITINCLUSION and property product.
    :param gitrepo:
    :param tags:
    :return:
    """
    errordata = {}

    try:
        workspace = config.get("GITCHANGELOG", "workspace_dir")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        included_paths = str(config.get("GITINCLUSION", "product")).split(",")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)
    return getdaywisecommithistory(gitrepo, fromdate, todate, included_paths, customer, workspace, branch)

def getdaywisecommithistory(gitrepo, fromdate, todate, includepath, customer, workspace, branch):
    """
        This will return git STATS FOR A DATE RANGE passed to methods
        :param gitrepo:
        :param tags:
        :param includepath:
        :return:
        """
    jsondata = {}
    errordata = {}

    # Put customer info in return json
    if customer is None:
        jsondata["product"] = True
        jsondata["customer"] = ""
        jsondata["tabulardata"] = [["File Name", "Status"]]
        errordata["product"] = True
        errordata["customer"] = ""
    else:
        jsondata["product"] = False
        jsondata["customer"] = customer
        jsondata["tabulardata"] = [["File Name", "Status"]]
        errordata["product"] = False
        errordata["customer"] = customer

    srcpath = workspace + os.path.sep + gitrepo

    try:
        check_output(["git", "fetch"], cwd=srcpath)
    except Exception as e:
        errordata["statuscode"] = 400
        errordata["errormsg"] = "exception occured while fetching repo from git. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        check_output(["git", "reset", "--hard"], cwd=srcpath)
    except Exception as e:
        errordata["statuscode"] = 400
        errordata["errormsg"] = "exception occured while hard restting repo from git. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        check_output(["git", "checkout", branch], cwd=srcpath)
    except Exception as e:
        errordata["statuscode"] = 400
        errordata["errormsg"] = "exception occured while checkoing put branch from git. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        stats = str(check_output(["git", "log", "--after=" + fromdate, "--before=" + todate, "--pretty=format:\"%H\":{\"commithash\":\"%H\",\"authorname\":\"%an\",\"authoremail\":\"%ae\",\"authordate\":\"%at\",\"committername\":\"%cn\",\"committeremail\":\"%ce\",\"committerdate\":\"%cd\"},"] + includepath, cwd=srcpath))
        stats = "{" + stats[2:-2]
        stats = stats.replace("\\n","")
        stats = stats + "}"
        stats=json.loads(stats)
    except Exception as e:
        errordata["errorcode"] = 400
        errordata[
            "errormsg"] = "exception occured while getting Daywise Git stats. Exception is " + e.__str__()
        return builderrorresponse(errordata)
    return getsuccessresponse(stats)

def getfileschangedforcommit(gitrepo, commitid):
    errordata = {}

    try:
        workspace = config.get("GITCHANGELOG", "workspace_dir")
    except Exception as e:
        errordata["statuscode"] = 404
        errordata["errormsg"] = "exception occured while reading config file. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    srcpath = workspace + os.path.sep + gitrepo
    try:
        check_output(["git", "fetch"], cwd=srcpath)
    except Exception as e:
        errordata["statuscode"] = 400
        errordata["errormsg"] = "exception occured while fetching repo from git. Exception is " + e.__str__()
        return builderrorresponse(errordata)

    try:
        filelist = str(check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "--oneline", commitid], cwd=srcpath))
        filelist = filelist[2:].split("\\n")
        jsondata = {"filelist": filelist}
    except Exception as e:
        errordata["statuscode"] = 400
        errordata["errormsg"] = "exception occured while fetching changed files from git for commitid" + commitid + ". Exception is " + e.__str__()
        return builderrorresponse(errordata)
    return getsuccessresponse(jsondata)

def getsuccessresponse(data):
    returndata = {}
    returndata["success"] = "true"
    returndata["data"] = data
    returndata["error"] = {}
    return json.dumps(returndata)

def builderrorresponse(data):
    returndata = {}
    returndata["success"] = "false"
    returndata["data"] = {}
    returndata["error"] = data
    return json.dumps(returndata)

def getpatchdiff(futurebranch, currentbranch, Release, build):
    data = check_output(['bash', "./gitdifflog.sh", futurebranch, currentbranch, Release, build])
    jsondata = {"Result": str(data)}
    return getsuccessresponse(jsondata)
