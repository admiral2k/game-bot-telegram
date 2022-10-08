class AccessError(Exception):
    """raise this when the user tries to access
    game variables when game isn't started"""
    pass


class ActionError(Exception):
    """raise this when the user tries to end/start the game
    when its already ended/started"""
    pass
