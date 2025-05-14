def scan(filename):
    valid_operators = {'+', '-', '*', '/', '.',".s"}
    tokens = []
    try:
        with open(filename, 'r') as f:
            content = f.read()
            for token in content.split():
                if token in valid_operators:
                    tokens.append(token)
                else:
                    try:
                        num = int(token)
                        tokens.append(num)
                    except ValueError:
                        print(f"invalid token: {token}")
                        return None
        return tokens
    except Exception as e:
        print(f"error: {e}")
        return None
