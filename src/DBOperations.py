import pymongo

def Init():
    client = pymongo.MongoClient('mongodb://localhost:27017/everLASTing')
    db = client['everLASTing']
    users = db['users']
    users.drop()
    users.insert_one({
        'id': '123',
        'nickname': 'Vaserman',
        'tests': {
            'test1': {
                'total': 10,
                'solved': 5,
                'level': 'medium',
                'ratio': 0.5
            }
        }
    })

Init()