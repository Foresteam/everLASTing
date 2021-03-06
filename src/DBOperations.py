from bson import Regex
import pymongo

def TestFinished(id: str, testName, level, solved=0, total=0, nickname: str = None):
    testData = {
        'solved': solved,
        'total': total,
        'ratio': solved / total
    }
    global users
    user = users.find_one({ 'id': id })
    if user:
        # break the previos result was better
        if testName in user['tests'] and level in user['tests'][testName] and user['tests'][testName][level]['ratio'] > testData['ratio']:
            return
    else:
        users.insert_one({
            'id': id,
            'nickname': nickname,
            'tests': {}
        })
    users.update_one({ 'id': id }, { '$set': { f'tests.{testName}.{level}': testData } })
    if nickname:
        users.update_one({ 'id': id }, { '$set': { 'nickname': nickname } })
def GetResultsByNickname(**kwargs) -> dict:
    global db
    rgx = Regex(f'.*({kwargs["nickname"]}).*', 'i')
    q = {
        'nickname': rgx,
        f'tests.{kwargs["name"]}': {'$exists': True}
    }
    if not kwargs['nickname']:
        del q['nickname']
    if not kwargs['name']:
        del q[f'tests.{kwargs["name"]}']
    results = db.users.find(q)
    return results

def Init():
    global client, db, users
	# connect to DB. Change this, if your DB URL is different
    client = pymongo.MongoClient('mongodb://localhost:27017/everLASTing')
    db = client['everLASTing']
    users = db['users']