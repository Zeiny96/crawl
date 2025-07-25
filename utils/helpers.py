def extract_key_paths(d):
    result = []

    def recurse(curr, path):
        if isinstance(curr, dict):
            for k, v in curr.items():
                recurse(v, path + [k])
        elif curr is not None:
            result.append(path)

    recurse(d, [])
    return result

