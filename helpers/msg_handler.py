def Debug_msg(flow, msg, type):
    if type == 0:
        return f'>> Debug <flow {flow}> : {msg}'
    elif type == 1:
        return f'>> Info log <flow {flow}> : {msg}'