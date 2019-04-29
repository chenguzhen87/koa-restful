const Koa = require('koa');
const cors = require('koa2-cors');
const convert = require('koa-convert')
const bodyParser = require('koa-bodyparser');
const checkToken = require('./middleware/check-token');
const routes = require('./routes');
const path = require('path')
const static = require('koa-static');
const app = new Koa();

app.use(bodyParser());
app.use(convert(checkToken()))
//跨域
app.use(cors({
    origin: function (ctx) {
        return "*"; // 允许来自所有域名请求
    },
    exposeHeaders: ['WWW-Authenticate', 'Server-Authorization'],
    maxAge: 5,
    credentials: true,
    allowMethods: ['GET', 'POST', 'DELETE'],
    allowHeaders: ['Content-Type', 'Authorization', 'Accept'],
}));

// 静态资源目录对于相对入口文件index.js的路径
const staticPath = './dist'

app.use(static(
    path.join( __dirname,  staticPath)
));

routes(app);

//端口监听
app.listen(3009);
console.info("start success")
