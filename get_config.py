import os, re, copy


def __get_config():
    try:
        txt = open(os.getcwd() + '/config.txt', 'r')
    except Exception as e:
        print(e)
        exit("programme has been exited")

    def regular(string):
        return re.match('^(#|\r?\n)', string) is None

    config_list_temp1 = map(lambda x: re.sub('/?\r?\n$', '', x), filter(regular, txt))
    config_list = map(lambda x: [re.sub(':.*?$', '', x), re.sub('^.*?:', '', x)], config_list_temp1)

    return list(config_list)


def get_apple_account():
    temp = __get_config()
    config = {}
    for i in temp:
        if str(i[0]).lower() == 'appleid' and i[1] != '':
            config['appleid'] = i[1]
        elif str(i[0]).lower() == 'password' and i[1] != '':
            config['password'] = i[1]

    if config.__len__() == 2:
        return config
    else:
        raise Exception('check your apple account info')


def get_form_config():
    temp = __get_config()
    form_name = ['shipping-user-lastName', 'shipping-user-firstName', 'shipping-user-daytimePhoneAreaCode',
                 'shipping-user-daytimePhone', 'shipping-user-street', 'shipping-user-street2',
                 'shipping-user-postalCode', 'shipping-user-emailAddress', 'shipping-user-mobilePhone']

    form_select_name = ['shipping-user-state', 'shipping-user-city', 'shipping-user-district']

    config = []
    for k, v in enumerate(temp):
        if v[0] in form_name:
            if (v[0] != 'shipping-user-mobilePhone' and v[1] != '') or v[0] == 'shipping-user-mobilePhone':
                v.append('fill')
                config.append(v)

        if v[0] in form_select_name:
            v.append('select')
            config.append(v)

    if config.__len__() == 12:
        return config
    else:
        raise Exception('check your config info')


if __name__ == '__main__':
    try:
        test1 = get_apple_account()
        test2 = get_form_config()
        print(test1)
        print(test2)
        exit('your config is alright')
    except  Exception as e:
        print(e)
