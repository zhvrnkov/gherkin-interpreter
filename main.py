scenario = """Given user is on start-screen
And user is not authorized
When user taps profile button
Then user goes to profile screen
""".splitlines()

Exp = (str, list)

keywords = ["on", "is", "Given"]

class Env(dict):

    @classmethod
    def default(cls):
        return cls({
            "on": lambda where: where,
            "is": lambda state: state,
            "start-screen": "start screen",
            "Given": Env.given_action,
            "user": None
        })

    @staticmethod
    def given_action(subject, envID):
        global current_env
        current_env = Env(Env.dictforid(envID), current_env)

    @staticmethod
    def dictforid(id: str) -> dict:
        return {
            "start screen": Env.startscreen_dict(),
            "profile screen": Env.profilescreen_dict()
        }[id]
    
    @staticmethod
    def startscreen_dict() -> dict:
        return {
            # "authorized": lambda: bool(random.getrandbits(1)), # authorization checker
            "profile button": "profile_button_element_id",
            # "profile screen": lambda: bool(random.getrandbits(1)) # profile screen presentation checker
        }

    @staticmethod
    def profilescreen_dict() -> dict:
        return {
            "avatar": "avatar_element_id",
            "logout button": "logout_button_id"
        }

    def __init__(self, dict, outer=None):
        self.update(dict)
        self.outer = outer
        
current_env = Env.default()

def parse(step: str) -> list:
    return read_from_tokens(tokenize(step))

def tokenize(step: str) -> list:
    return step.split()

def read_from_tokens(tokens: list) -> Exp:
    if len(tokens) == 1:
        return str(tokens[0])
    exps = []
    l = exps
    for token in tokens:
        if token not in keywords:
            l.append(token)
        elif len(l) == 0:
            l.append(token)
        else:
            l.append([token])
            l = l[-1]
    return exps
    
def eval(exp: Exp):
    env = current_env
    if isinstance(exp, str):
        return env[exp]
    else:
        op, *args = exp
        proc = eval(op)
        args = [eval(arg) for arg in args]
        print(args)
        return proc(*args)

    
