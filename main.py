scenario = """Given user is-on start screen
And user is not authorized
When user taps profile button
Then user goes to profile screen
""".splitlines()

Exp = (str, list)

class Env(dict):

    @classmethod
    def default(cls):
        return cls({
            "is-on": lambda where: where(),
            "is": lambda state: state()  
        })
    
    @staticmethod
    def startScreenDict() -> dict:
        return {
            # "authorized": lambda: bool(random.getrandbits(1)), # authorization checker
            "profile button": "profile_button_element_id",
            # "profile screen": lambda: bool(random.getrandbits(1)) # profile screen presentation checker
        }

    @staticmethod
    def profileScreenDict(outerEnv = None) -> dict:
        return {
            "avatar": "avatar_element_id",
            "logout button": "logout_button_id"
        }

    def __init__(self, dict, outer=None):
        self.update(dict)
        self.outer = outer

currentEnv = Env.default()

gherkinKeywords = ["Given", "user", "When", "Then"]
keywords = ["is-on", "is", "not", "taps", "goes"]

def parse(step: str) -> list:
    return read_from_tokens(tokenize(step))

def tokenize(step: str) -> list:
    return step.split()

def read_from_tokens(tokens: list) -> Exp:
    exp = []
    l = exp
    for token in tokens:
        if token in keywords:
            _l = [token]
            l = _l
            exp.append(_l)
        else:
            l.append(token)
    return exp
    
def eval(exp: Exp, env: Env):
    pass
