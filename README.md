# jksb-zzu

本项目实现了针对郑州大学师生健康上报平台的每日定时自动健康申报，并可通过email自动发送申报结果。本项目通过Github Actions定期执行，无需开启电脑或租用服务器。

**受网络状况和Github服务器的影响，申报结果存在不确定性，请谨慎使用**

## 任务流程

1. 登录郑州大学统一身份认证平台账号
2. 沿用上一次提交的填报内容，并将健康码状态选择为绿码
3. 提交申报


## 技术方案

- python+selenium+firefox
- 通过Github Action定期执行自动申报代码

## 项目配置

### 0. 创建一个Github账号

自动申报的结果将通过email发送到注册该账号所用的邮箱。

### 1. 生成自己的仓库

点击右上角的Fork按钮，将代码fork到自己的仓库。

### 2. 填写账号密码

2.1 在fork出来的仓库中点击最右侧的Settings，然后在左侧竖栏中选择Secrets。

2.2 点击右上角的New repository secret按钮，在Name一栏填入`ID`(*注意需要大写*),在Value一栏填入你的用户号，点击Add secret保存。

2.3 再次点击右上角的New repository secret按钮，在Name一栏填入`PASSWORD`(*注意需要大写*),在Value一栏填入你的密码，点击Add secret保存。

### 3. 定时运行

点击位于Settings同一栏的Actions，确认启用workflow后，选择名字为jksb的工作流，启用。

默认配置为，每天 22:47 UTC (*我们这里是UTC +8，相当于6：47 a.m.*)运行。

控制Github Action自动运行的文件是/.github/workflows/jksb.yml，如需修改定时运行时间，则修改该文件的`- cron:  '47 22 * * *'`一行，修改方法可参考[该文档](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#scheduled-events)。

### 4. 修改Github Actions的通知方式

Github默认当Action执行成功时不通知，执行失败时邮件通知。

修改方式如下：
4.1 点击右上角自己的头像，选择Settings
4.2 在左侧竖栏中选择Notifications，下拉找到Actions一栏
4.3 取消勾选Send notifications for workflows only

### 5. 手动测试（可选）

在自己仓库的Actions一栏中选择jksb工作流，点击右下角的Run workflow可手动运行，以测试能否正确填报。

如出错，可在该次运行结果的右侧`...`中选择View workflow file，再点击左侧的build以查看报错信息。

### 6. 批量申报（可选）

在添加`ID`和`PASSWORD`时，可以空格为分割，按顺序填入多组账号密码（数量不限），程序会自动依次申报。

例如，在需要申报ID为001密码为111，和ID为002密码为222的账号时，`ID`填写为“001 002”，`PASSWORD`填写为“111 222”.

## 免责声明

使用本软件直接或间接造成的损失由使用者承担，请谨慎使用。

如遇身体不适，健康码颜色变化或居住地址发生变化等情况，请及时更新健康申报信息。

## 致谢

本项目的框架和流程参考[@Editi0](https://github.com/Editi0)的[jksb_sysu](https://github.com/Editi0/jksb_sysu)项目，该项目最早由 [@tomatoF](https://github.com/tomatoF) 开发。