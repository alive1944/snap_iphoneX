from splinter import Browser
import get_config
import time

reurl = ''
func_name = ''

show_error = False


def start():
    # iPhoneX网址 已选择好所有机身参数
    # url = "https://www.apple.com/cn/shop/buy-iphone/iphone-x/5.8-%E8%8B%B1%E5%AF%B8%E6%98%BE%E7%A4%BA" \
    #       "%E5%B1%8F-256gb-%E6%B7%B1%E7%A9%BA%E7%81%B0%E8%89%B2#00,11,21"

    # 测试网址 iPhone7Plus 256G
    # url = "https://www.apple.com/cn/shop/buy-iphone/iphone-7/5.5-%E8%8B%B1%E5%AF%B8%E5%B1%8F%E5%B9%95-128" \
    #       "gb-%E9%87%91%E8%89%B2#01,13,21"
    url = get_config.get_url()
    b = Browser('chrome')

    def browser():
        count = 0
        try:
            # 打开浏览器
            loop_click(b, url)
        except Exception as e:
            b.visit(globals()['reurl'])
            globals()['func_name'](b)
            try_print('too much error,retry')
            if count == 5:
                print('a fatal error occurred,reopen the browser')
                b.quit()
                try_print(e)
                browser()
                count = 0
            count += 1

    browser()


# 循环刷新点击预售
def loop_click(b, url):
    b.visit(url)
    while True:
        before_click = b.url
        try_action(b.find_by_css, '.as-button-large')
        after_click = b.url

        # 当点击跳转生效时，url改变，则退出循环
        if before_click != after_click:
            break

        print("尚未开售,当前时间--", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # 按钮未开放点击(未开售)，刷新页面
        b.reload()

    step_to_step(b, before_click)


def step_to_step(b, _url):
    set_url(b, _url)
    cart_span = b.find_by_css('.add-to-cart')
    cart_button = cart_span.find_by_tag('button')
    cart_button.click()
    _url = b.url
    try_action(b.find_by_id, 'cart-actions-checkout')
    login(b, _url)


def login(b, _url):
    set_url(b, _url)
    config = get_config.get_apple_account()
    try_(b.fill, 'login-appleId', config['appleid'])
    try_(b.fill, 'login-password', config['password'])
    _url = b.url
    try_action(b.find_by_id, 'sign-in')

    first_step(b, _url)


def first_step(b, _url):
    set_url(b, _url)
    print('first step')
    _url = b.url
    try_action(b.find_by_id, 'cart-continue-button')
    second_step(b, _url)


def second_step(b, _url):
    # second step
    set_url(b, _url)
    print('second step')
    form_value = get_config.get_form_config()
    for i in form_value:
        try_(getattr(b, i[2]), i[0], i[1])

    _url = b.url
    try_action(b.find_by_id, 'shipping-continue-button')
    third_step(b, _url)


def third_step(b, _url):
    # third step
    set_url(b, _url)
    print('third step')
    try_(b.choose, 'payment-form-options-bankOption', 'Alipay')
    _url = b.url
    try_action(b.find_by_id, 'payment-continue-button')
    forth_step(b, _url)


def forth_step(b, _url):
    # forth step
    set_url(b, _url)
    print('firforthst step')
    try_(b.choose, 'invoice-form-options', 'personal')
    _url = b.url
    try_action(b.find_by_id, 'invoice-next-step')
    last_step(b, _url)


def last_step(b, _url):
    # last step
    set_url(b, _url)
    print('last step')
    try_action(b.find_by_id, 'terms-accept')
    _url = b.url
    try_action(b.find_by_id, 'terms-continue-button')
    place_order(b, _url)


def place_order(b, _url):
    pass
    # place order
    try_action(b.find_by_id, 'place-order-button')


def try_(func, name, value=''):
    print('try fill element:' + name)
    count = 0
    while True:
        try:
            func(name, value)
            time.sleep(0.2)
            print('filled accessfully!\n')
            break
        except Exception as e:
            if count == 3:
                raise Exception('too much fill tried')

            try_print(e)
            count += 1
        time.sleep(0.5)


def try_action(func, name, action='click'):
    print('try ' + action + ' element:' + name)
    count = 0
    while True:
        try:
            obj = func(name)
            if action == 'click':
                obj.click()
            elif action == 'check':
                obj.check()

            time.sleep(0.2)
            print(action + ' action\n')
            break
        except Exception as e:
            if count == 3:
                raise Exception('too much action tried')

            try_print(e)
            count += 1
            time.sleep(0.5)


def set_url(b, _url, flag=''):
    while b.url == _url:
        if flag != '':
            print(1)
        time.sleep(0.1)
        pass

    globals()['reurl'] = b.url
    globals()['func_name'] = login


def try_print(str):
    if globals()['show_error'] is True:
        print(str)


if __name__ == '__main__':
    if get_config.test_config() is not True:
        print(get_config.test_config())
        exit('programme has been exited')

    start()
    time.sleep(10000)
