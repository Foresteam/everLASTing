import pymongo

def TestSolved(id: str, testName, level, solved=0, total=0, nickname: str = None):
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

def Init():
    global client, db, users
    client = pymongo.MongoClient('mongodb://localhost:27017/everLASTing')
    db = client['everLASTing']
    users = db['users']
    users.drop()
    users.insert_one({
        'id': '123',
        'nickname': 'Vaserman',
        'tests': {
            'test1': {
                'medium': {
                    'total': 10,
                    'solved': 5,
                    'ratio': 0.5
                }
            }
        }
    })
    TestSolved('123', 'test1', 'hard', { 'total': 1, 'solved': 2 }, nickname='anonymous')

Init()