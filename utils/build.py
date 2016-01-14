import base64, hashlib, pickle

class Rule(object):
    def __init__(self, deps):

def source(src):
    if isinstance(src, dict):
        return src
    return {
        "language": guess_src_lang(os.path.splitext(src)[1]),
        "filename": src,
        "cflags": _,
    }

def hash_value(value, length=32):
    h = hashlib.sha512(pickle.dumps(value)).digest()
    h = base64.b32encode(h).decode("ascii").lower().rstrip("=")[:length]
    return h

def executable(srcs, out_fn, cargs):
    rules = RuleSet()
    rule_ids = []
    for src in map(source, src):
        rule_id = _
        rules.add_rule(

            "type": "target",
            "dependencies": raw_src(src["filename"]),
            "name": src["filename"],
            "extension": ".o"
            "action": lambda: compile_src(src["filename"], **kwargs),
        )
        rule_ids.append(rule_ids)
    rules[("link", frozen_kwargs, rule_id)] = {
        "type": "target",
        "dependencies": rule_id,
        "name": _,
        "extension": _,
        "action": _,
    }
    return rules

class RuleSet(object):
    def __init__(self, rules={}):
        self.rules = dict(rules)

    def add_rule(self, *args, **kwargs):
        self.rules[rule["id"]] = rule

class Action(object):
    @property
    def id(self):
        raise NotImplementedError()
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

class FileAction(Action):
    id = "FileAction"
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

def rule(action, name="", ext="", deps=()):
    if ext and not ext.startswith("."):
        ext = "." + ext
    rule = {
        "deps": set(dep["id"] for dep in deps),
        "name": name,
        "ext": ext,
        "action": action.id,
    }
    rule["id"] = hash_value(rule)
    rule["action"] = action
    return rule

def is_out_of_date(out_fn, dep_fns):
    out_mtime = os.path.getmtime(out_fn)
    for dep_fn in dep_fns:
        dep_mtime = os.path.getmtime(dep_fn)
        if dep_mtime > out_mtime:
            return True
    return False
