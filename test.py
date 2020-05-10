from requests import get, post, delete, put


print(get('http://127.0.0.1:8080/api/jobs').json())
print(get('http://127.0.0.1:8080/api/users').json())
print(put('http://127.0.0.1:8080/api/users/2', json={'age': '123'}).json())
print(delete('http://127.0.0.1:8080/api/users/4').json())
