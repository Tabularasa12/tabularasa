
REGEX = dict(
    apps = "^[a-zA-Z][a-zA-Z0-9 -_àçéèêëïöôùüû]+$",
    controllers = "^[a-zA-Z0-9]+(.py)$",
    # controllers = "^(start|end)_[0-9]{1,2}_[a-zA-Z0-9]+(.py)$",
    name_begin_by_letter = "^[a-zA-Z].+$",
    name_alphanumeric = "^[a-zA-Z][a-zA-Z0-9_]+$",
    color = "^#[a-f0-9_]{6}$",
    ressources = "^[a-zA-Z][a-zA-Z0-9 -_]+(.py)$",
)