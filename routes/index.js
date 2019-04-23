const Router = require('koa-router');
const router = new Router();

const user = require('./sysmgr/user');
const role = require('./sysmgr/role');
const menu = require('./sysmgr/menu');
const login = require('./monitor/login-log');

module.exports = function (app){
    //路由表
    app.use(router.routes()).use(router.allowedMethods());

    //sysmgr
    router.use('/apis/sysmgr/user',user.routes(),user.allowedMethods());
    router.use('/apis/sysmgr/role',role.routes(),role.allowedMethods());
    router.use('/apis/sysmgr/menu',menu.routes(),menu.allowedMethods());

    //monitor
    router.use('/apis/monitor/loginlog',login.routes(),login.allowedMethods());
};
