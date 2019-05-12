import os
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'tests'
app.config['MONGO_URI'] = os.environ.get('MONGO_URL') or 'mongodb://localhost:27017/tests'
mongo = PyMongo(app)
CORS(app)


@app.route('/api/id', methods=['POST'])
def get_id():
    return jsonify(id=str(ObjectId()))


@app.route('/api/tests', methods=['POST'])
def get_test_list():
    """
    Вернуть список имен тестов с id
    :return: список имен тестов с id
    """

    tests = mongo.db.tests.find()
    result = []
    for test in tests:
        result.append({
            'id': str(test['_id']),
            'name': test['name'],
        })
    return jsonify(result)


@app.route('/api/get/<id>', methods=['POST'])
def get_test(id):
    """
    Вернуть тест с id
    :param id: id теста
    :return: тест
    """

    test = mongo.db.tests.find_one({'_id': id})
    result = {
        'id': str(test['_id']),
        'name': test['name'],
        'questions': test['questions']
    }
    return jsonify(result)


@app.route('/api/save/<id>', methods=['POST'])
def save_test(id):
    """
    Сохранить тест (добавить новый, если не найден, либо обновить уже существующий)
    :param id: id теста
    :return: результат операции сохранения
    """

    test_data = request.get_json()
    is_exist = mongo.db.tests.find_one({'_id': id})
    if is_exist:
        mongo.db.tests.update(
            {'_id': id},
            {'$set': {
                'name': test_data['name'],
                'questions': test_data['questions']
            }}
        )
        msg = 'record updated'
    else:
        mongo.db.tests.insert_one({
            '_id': test_data['id'],
            'name': test_data['name'],
            'questions': test_data['questions']
        })
        msg = 'record added'
    return jsonify(msg)


@app.route('/api/delete/<id>', methods=['POST'])
def delete_test(id):
    """
    Удалить тест с id
    :param id: id теста
    :return результат операции удаления
    """

    result = mongo.db.tests.delete_one({'_id': id})
    msg = 'record with id %s deleted' % id if result.deleted_count == 1 else 'record not found'
    return jsonify(msg)


if __name__ == '__main__':
    app.run(debug=True)