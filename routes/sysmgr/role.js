require('dotenv').load();
require('dotenv').config();

const Router = require('koa-router');
const router = new Router();
const db = require('../../db/index');
const {Role} = require('../../models/sysmgr');

router
    .get('/getList',async(ctx)=> {
        await Role.findAll({}).then(roles => {
            // 用户名存在通过验证
            ctx.response.status = 200;
            ctx.response.body = {roles: roles, msg: '请求成功'};
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '登录失败，请于管理员联系或稍后重试'};
        });
    })
    .post('/add',async(ctx)=> {
        let name = ctx.request.body.name;
        let descript = ctx.request.body.descript;
        await Role.create({
            name: name,
            descript: descript
        }).then(data => {
            // 用户名存在通过验证
            ctx.response.status = 200;
            ctx.response.body = {msg: '添加成功'};
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '登录失败，请于管理员联系或稍后重试'};
        });
    })
    .post('/update',async(ctx)=> {
        let id = ctx.request.body.id;
        let name = ctx.request.body.name;
        let descript = ctx.request.body.descript;
        await Role.update({
            name: name,
            descript: descript
        },{
            where:{'id': id}
        }).then(data => {
        ctx.response.status = 200;
        ctx.response.body = {msg: '修改成功'};
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '登录失败，请于管理员联系或稍后重试'};
        });
    })
    .delete('/delete',async(ctx)=> {
        let id = ctx.request.query.id;
        await Role.destroy({
            where:{'id': id}
        }).then(data => {
            ctx.response.status = 200;
            ctx.response.body = {msg: '删除成功'};
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '登录失败，请于管理员联系或稍后重试'};
        });
    });
module.exports = router;
