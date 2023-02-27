def urljoin(*args):
    args = filter(None, args)
    return "/".join(map(lambda x: str(x).rstrip('/'), args))
