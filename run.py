#菜单
def menu():
    print('*' * 40)
    print('*' * 10, '欢迎来到图书管理系统 1.0 ')
    print('*' * 40)
    print('请选择：')
    print("1: 注册新用户：")
    print("2. 进行图书馆操作：")
    print("3. 退出本系统")

# 用户与管理者
def while_user(name):
    while name:  # 根据是否登陆成功，进入用户菜单

        if name == 'fxm':  # 判断是否为管理者
            manger()  # 管理者页面
            manger_n = input()
            if manger_n == '1':
                del_user()  # 删除一个用户
            elif manger_n == '2':
                edit_user()  # 修改用户密码
            elif manger_n == '3':
                look_user()  # 查看一个用户信息
            elif manger_n == '4':
                look_users()  # 查看全部用户信息
            elif manger_n == '5':
                break  # 退出管理者页面
            else:
                print("非法输入！！！")
                print("请再次选择：")

        else:
            user_menu(name)  # 普通用户页面
            user_n = input()
            if user_n == '1':
                add_book()  # 添加书籍
            elif user_n == '2':
                del_book()  # 删除书籍
            elif user_n == '3':
                edit_book()  # 修改书籍信息
            elif user_n == '4':
                look_book()  # 查询单本书籍信息
            elif user_n == '5':
                look_books()  # 查询所有书籍信息
            elif user_n == '6':
                break  # 退出普通用户页面
            else:
                print("非法输入！！！")
                print("请再次选择：")
def user_menu():
    print('*' * 40)
    print('请选择您所需的功能：')
    print('1. 添加书籍')
    print('2. 删除书籍')
    print('3. 修改书籍信息')
    print('4. 查询单本书籍信息')
    print('5. 查询所有书籍信息')
    print('6. 退出您的图书小屋')

if __name__ == "__main__":
    sqlApi = SqlApi()
    
        # 循环菜单主页面
    while True:
        menu()  # 主菜单页面
        menu_n = input()
        if menu_n == '1':
            name=input()
            sqlApi.register(name)
        elif menu_n == '2':
            user_menu()
            choose=input()
            sqlApi.
        elif menu_n == '3':
            print("谢谢惠顾")
            break
        else:
            print("非法输入！！！")
            print("请再次选择：")