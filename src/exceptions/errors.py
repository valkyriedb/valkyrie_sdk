class ValkyrieError(Exception):
    pass

class ValkyrieConnectionError(ValkyrieError):
    pass

class ValkyrieRequestError(ValkyrieError):
    pass

class ValkyrieServerError(ValkyrieError):
    pass

class ValkyrieAuthError(ValkyrieError):
    pass