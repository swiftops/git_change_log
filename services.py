from flask import Flask, request
from com.swiftops.changelog.methods import GitChangeLog as changelog
import connexion

app = Flask(__name__)
app = connexion.App(__name__)
app.add_api('swagger.yaml')


@app.route('/api/gitchangelog/v1/shortstat/<gitrepo>/<tags>', methods=['GET'])
def getproductshortstat(gitrepo, tags):
    """
        This api will return git short stat from given tags only for product sourcecode mentioned in gitconfig.ini for section GITINCLUSION and property product.
        :param gitrepo: salm_core OR salm_automation
        :param tags: 3.2.0_12..3.2.0_13
        :return:
        """
    short_stats = changelog.getproductshortstat(gitrepo, tags)
    return short_stats


@app.route('/api/gitchangelog/v1/shortstat/<customer>/<gitrepo>/<tags>', methods=['GET'])
def getcustomshortstat(customer, gitrepo, tags):
    """
       This api will return git short stat for given tags only for custom sourcecode.
       This custom mapping mentioned in gitconfig.ini for section GITINCLUSION and property custom.
       :param gitrepo:
       :param tags:
       :param customer:
       :return:
       """
    short_stats = changelog.getcustomshortstat(gitrepo, tags, customer)
    return short_stats


@app.route('/api/gitchangelog/v1/fileschanged/<gitrepo>/<tags>', methods=['GET'])
def getproductchangedfiles(gitrepo, tags):
    """
        This api will return git changed files set for given tags only from product sourcecode mentioned in gitconfig.ini for section GITINCLUSION and property product.
        :param gitrepo:
        :param tags:
        :return:
        """
    files_changed = changelog.getproductchangedfiles(gitrepo, tags)
    return files_changed


@app.route('/api/gitchangelog/v1/fileschanged/<customer>/<gitrepo>/<tags>', methods=['GET'])
def getcustomchangedfiles(customer, gitrepo, tags):
    """
        This api will return git changed files set for given tags only from custom sourcecode mentioned in gitconfig.ini for section GITINCLUSION and property customer.
        :param gitrepo:
        :param tags:
        :param customer:
        :return:
        """
    files_changed = changelog.getcustomchangedfiles(gitrepo, tags, customer)
    return files_changed


@app.route('/api/gitchangelog/v1/gitlog/', methods=['POST'])
def getdaywiseproductstats():
    """
       This will return day wise git log for branch passed to methods.
       :param gitrepo:
       :param tags:
       :param includepath:
       :return:
       """
    if request.method == 'POST':
        req_data = request.get_json()
        gitrepo = req_data['data']['gitrepo']
        fromdate = req_data['data']['fromdate']
        todate = req_data['data']['todate']
        branch = req_data['data']['branch']
        customer = req_data['data']['customer']
        gitlog = changelog.getdaywiseproductstats(gitrepo, fromdate, todate, branch, customer)
    return gitlog


@app.route('/api/gitchangelog/v1/gitfileschanged/', methods=['POST'])
def getfileschangedforcommit():
    """
        This api will return git changed files set for given commit-id.
        :param gitrepo:
        :param commitid:
        :return:
        """
    if request.method == 'POST':
        req_data = request.get_json()
        gitrepo = req_data['data']['gitrepo']
        commitid = req_data['data']['commitid']
        fileslist = changelog.getfileschangedforcommit(gitrepo, commitid)
    return  fileslist

@app.route('/api/gitchangelog/v1/gitdifflog/', methods=['POST'])
def getdifflog():
    req_data = request.get_json()
    futurebranch = req_data['data']['futurebranch']
    currentbranch = req_data['data']['currentbranch']
    Release = req_data['data']['Release']
    build = req_data['data']['build']
    return changelog.getpatchdiff(futurebranch, currentbranch, Release, build)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)