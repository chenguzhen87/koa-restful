require('dotenv').load();
require('dotenv').config();

const Router = require('koa-router');
const router = new Router();
const db = require('../../db/index');
const {LoginLog} = require('../../models/monitor');
const Sequelize = require('sequelize')
router
    .get('/getPageList',async(ctx,next)=> {
        await LoginLog.findAndCountAll({
            offset: 0,
            limit: 10
        }).then(result => {
            // 用户名存在通过验证
            ctx.response.status = 200;
            ctx.response.body = {data: result, msg: '请求成功'};
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '登录失败，请于管理员联系或稍后重试'};
        });
    });
module.exports = router;
