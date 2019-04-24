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
# pm2 kill                      # 杀掉所有pm2进程并释放资源，包含pm2自身，会释放端口

更多pm2用法请参考https://bitcoin-on-nodejs.ebookchain.org/4-%E5%BC%80%E5%8F%91%E5%AE%9E%E8%B7%B5/5-%E9%83%A8%E7%BD%B2/2-%E7%94%9F%E4%BA%A7%E7%8E%AF%E5%A2%83%E4%B8%8B%E7%9A%84pm2%E9%83%A8%E7%BD%B2.html

