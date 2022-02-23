import redis

r = redis.StrictRedis(host='192.168.2.155', port=6379, db=1)
print ("set key1 123")
print (r.set('key1', '123'))
print ("get key1")
print(r.get('key1'))
print(r.delete('key1'))
