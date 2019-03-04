import user_utils as users


def see_users_test():
    userUtils = users.UserUtils()
    value = userUtils.get_users_logged()
    print(value)


if __name__ == '__main__':
    see_users_test()
