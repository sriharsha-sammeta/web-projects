import boto3
import time, datetime
from boto3.dynamodb.conditions import Key, Attr


TABLE_NAME_FOOD = 'medicalbot-food'
def get_dynamodb():
    client = boto3.resource('dynamodb',
            region_name="us-east-1",
            )
    return client

def put_item_food(name, food, calories):
    client = get_dynamodb()
    table = client.Table(TABLE_NAME_FOOD)
    response = table.put_item(
        Item={
            'id': name,
            'food': food,
            'calories': calories,
            'timestamp': str(int(time.time()))
        })

def get_item_food(name, timestamp):
    client = get_dynamodb()
    table = client.Table(TABLE_NAME_FOOD)
    response = table.get_item(
        Key={
            'id': name,
            'timestamp':timestamp}
        )
    item = response['Item']
    print(item)
    #timestamp = item['timestamp']
    #weight = item['weight']
    #return (timestamp, weight)

def query_food(name):
    today = time.mktime(datetime.date.today().timetuple())
    tomorrow = today + 86400
    client = get_dynamodb()
    table = client.Table(TABLE_NAME_FOOD)
    response = table.query(
        KeyConditionExpression=Key('id').eq(name) & Key('timestamp').between(str(today), str(tomorrow))
    )
    if response['Count'] == 0:
        return None, None

    items = response['Items']
    food = []
    cals = []
    for item in items:
        food.append(item['food'])
        cals.append(int(item['calories']))
    return (food, cals)

def main():
    name = 'violet'
    #put_item_weight('violet', '54')
    #get_item_weight('violet')
    #query_weight(name)
    #put_item_food('violet', 'egg', '74')
    #get_item_food('violet', '1525485833')
    query_food(name)

if __name__ == '__main__':
    main()
