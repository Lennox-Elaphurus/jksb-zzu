# jksb-zzu

本项目采用了 GitHub Actions，可以实现每天定时自动健康申报，并由Github向注册Github账号的邮箱发送Action的执行结果。

**可正确运行，但由于受网络状况和Github服务器的影响，申报结果仍存在不确定性，请谨慎使用**

本项目修改自[@Editi0](https://github.com/Editi0)的[jksb_sysu](https://github.com/Editi0/jksb_sysu)项目，该项目最早由 [@tomatoF](https://github.com/tomatoF) 开发。

## 技术方案

- python+selenium+firefox
- 通过Github Action定时执行自动申报代码，无需租用服务器或长时间开启电脑。

## 项目配置

### 1. 生成自己的仓库

点击右上角的Fork按钮，将代码fork到自己的仓库。

### 2. 填写账号密码

2.1 在fork出来的仓库中点击最右侧的Settings，然后在左侧竖栏中选择Secrets。

2.2 点击右上角的New repository secret按钮，在Name一栏填入`ID`(*注意需要大写*),在Value一栏填入你的用户号，点击Add secret保存。

2.3 再次点击右上角的New repository secret按钮，在Name一栏填入``PASSWORD``(*注意需要大写*),在Value一栏填入你的密码，点击Add secret保存。

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

## 免责声明

使用本软件直接或间接造成的损失由使用者承担，请谨慎使用。

如遇身体不适，健康码颜色变化或居住地址发生变化等情况，请及时更新健康申报信息。