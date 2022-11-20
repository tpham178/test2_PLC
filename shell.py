import hello

while True:
    text = input('hello > ')
    result, error = hello.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)