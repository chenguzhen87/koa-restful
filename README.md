# koa restful

> A koa restful project

## development environment

``` bash
# install dependencies
npm install
# start server
node ./app.js

## production environment

# install pm2
npm npm install -g pm2
# set linux env
export JWT_SECRET=salt

# start server
pm2 start app.js --name koa-restful -i 1
# --name                 # 命名进程
# -i                     # 启动进程数
# pm2 list               # 显示所有进程状态

