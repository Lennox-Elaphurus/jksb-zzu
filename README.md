# jksb-zzu

修改自[@Editi0](https://github.com/Editi0)的[jksb_sysu](https://github.com/Editi0/jksb_sysu)项目，该项目最早由 [@tomatoF](https://github.com/tomatoF) 开发。适配了 GitHub Actions，可以实现每天定时运行，并由Github向注册Github账号的邮箱发送Action的执行结果。

**已可以正常运行，仍存在较大不确定性，谨慎使用**

## 技术方案

python+selenium+firefox。

## 项目配置

### 1. 生成自己的仓库

点击右上角的Fork按钮，将代码fork到自己的仓库

### 2. 填写账号密码

2.1 在fork出来的仓库中点击最右侧的Settings，然后在左侧竖栏中选择Secrets。

2.2 点击右上角的New repository secret按钮，在Name一栏填入`ID`(*注意需要大写*),在Value一栏填入你的用户号，点击Add secret保存。

2.3 再次点击右上角的New repository secret按钮，在Name一栏填入``PASSWORD``(*注意需要大写*),在Value一栏填入你的密码，点击Add secret保存。

### 3. 定时运行

默认配置为每天 22:47 UTC *(我们这里是UTC +8，相当于6：47 a.m.)*运行。

控制Github Action自动运行的文件是/.github/workfolows/jksb.yml，如需修改定时运行时间，则修改该文件的`- cron:  '47 22 * * *'`一行，修改方法可参考[该文档](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#scheduled-events)。

## 免责声明

使用软件过程中，发生意外造成的损失由使用者承担。如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。
