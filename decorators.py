def singleton(the_class):
    instances: dict = {}

    def get_class(*args, **kwargs):
        user: str = kwargs['user']
        if user not in instances:
            instances[user] = the_class(*args, **kwargs)

        return instances[user]

    return get_class
