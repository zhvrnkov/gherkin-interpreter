import random

scenario = """Given user is on start-screen
And user is not authorized
When user taps profile-button
Then user goes to profile-screen
""".splitlines()

Exp = (str, list)

keywords = ["on", "is", "Given", "And", "not", "When", "taps", "Then", "goes", "to"]

def print_ret(thing_to_print, thing_to_ret):
    print(thing_to_print)
    return thing_to_ret

class Env(dict):

    @classmethod
    def default(cls):
        return cls({
            "Given": Env.given_action,
            "user": None,
            "is": lambda state: state,
            "on": lambda where: where,
            "start-screen": "start screen",
            "And": Env.and_action,
            "not": lambda b: not b(),
            "authorized": lambda: print_ret(f'authoried: {True}', True),
            "When": Env.when_action,
            "taps": lambda elementID: print_ret(f'taps {elementID}', elementID),
            "Then": Env.then_action,
            "goes": lambda where: print_ret(f'goes to {where()}', where()),
            "to": lambda where: where
        })

    @staticmethod
    def given_action(subject, envID):
        print(f'given_action({subject}, {envID})')
        global current_env
        current_env = Env(Env.dictforid(envID), current_env)

    @staticmethod
    def and_action(subject, exp_result):
        print(f'and_action({subject}, {exp_result})')

    @staticmethod
    def when_action(subject, exp_result):
        print(f'when_action({subject}, {exp_result})')

    @staticmethod
    def then_action(subject, exp_result):
        print(f'when_action({subject}, {exp_result})')
        
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
            "profile-button": "profile_button_element_id",
            "profile-screen": lambda: bool(random.getrandbits(1)) # profile screen presentation checker
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

    def find(self, var):
        return self[var] if (var in self) else self.outer.find(var)
        
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
        return env.find(exp)
    else:
        op, *args = exp
        proc = eval(op)
        args = [eval(arg) for arg in args]
        return proc(*args)

def repl(prompt = 'BDD> '):
    while True:
        val = eval(parse(input(prompt)))
    
