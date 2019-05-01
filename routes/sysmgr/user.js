require('dotenv').load();
require('dotenv').config();

const Router = require('koa-router');
const router = new Router();
const {User} = require('../../models/sysmgr');
const {LoginLog} = require('../../models/monitor');
const {createToken,clearToken} = require('../../utils/token');
const Sequelize = require('sequelize');
const Op = Sequelize.Op;
const sha1 = require('sha1'); //加密


router
    .post('/login',async(ctx)=> {
        let user_name = ctx.request.body.user_name;
        let password = sha1(ctx.request.body.password);
        await User.findOne({
            where: {
                user_name: user_name,
                password: password
            }
        }).then(user => {
            if (user && (password === user.password)) {
                // 用户名存在通过验证
                ctx.response.status = 200;
                ctx.response.body = {user: user, token: createToken(user_name), msg: '请求成功'};
            } else {
                // 用户名或者密码错误没有通过验证，要么重新输入，要么点击注册
                ctx.response.status = 400;
                ctx.response.body = {msg: '用户名或密码错误'};
            }
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '登录失败，请于管理员联系或稍后重试'};
        }).finally(() => {
            LoginLog.create({
                user_name: user_name,
                ip: '127.0.0.1',
                descript: '登入'
            });
        });
    })
    .post('/logout',async(ctx)=> {
        let user_name = ctx.state.user_name;
        await clearToken(user_name).then(data => {
            ctx.response.status = 200;
            ctx.response.body = {msg: '操作成功'};
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '登录失败，请于管理员联系或稍后重试'};
        }).finally(() => {
            LoginLog.create({
                user_name: user_name,
                ip: '127.0.0.1',
                descript: '登出'
            });
        });
    })
    .get('/getPageList',async(ctx,next)=> {
        let current_page = Number.parseInt(ctx.request.query.current_page);
        let page_size = Number.parseInt(ctx.request.query.page_size);
        let user_name = ctx.request.query.user_name;
        let start_index = (current_page - 1) * page_size;
        let where = {};
        if(user_name !== ''){
            where["user_name"] = {[Op.substring]:user_name};
        }
        await User.findAndCountAll({
            offset: start_index,
            limit: page_size,
            where: where
        }).then(result => {
            // 用户名存在通过验证
            ctx.response.status = 200;
            ctx.response.body = {data: result, msg: '请求成功'};
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '请求失败，请于管理员联系或稍后重试'};
        });
    })
    .post('/add',async(ctx)=> {
        let user_name = ctx.request.body.user_name;
        let password = sha1('123456');
        let descript = ctx.request.body.descript;
        await User.create({
            user_name: user_name,
            password: password,
            descript: descript
        }).then(data => {
            if (data) {
                // 用户名存在通过验证
                ctx.response.status = 200;
                ctx.response.body = {msg: '操作成功'};
            } else {
                // 用户名或者密码错误没有通过验证，要么重新输入，要么点击注册
                ctx.response.status = 400;
                ctx.response.body = {msg: '操作失败，请于管理员联系或稍后重试'};
            }
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(222222,err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '操作失败，请于管理员联系或稍后重试'};
        });
    })
    .post('/update',async(ctx)=> {
        let user_name = ctx.request.body.user_name;
        let descript = ctx.request.body.descript;
        let pram = {user_name: user_name,descript: descript}
        await User.update(
            pram,{
                'where':{'user_name':user_name}
        }).then(data => {
            if (data) {
                // 用户名存在通过验证
                ctx.response.status = 200;
                ctx.response.body = {msg: '操作成功'};
            } else {
                // 用户名或者密码错误没有通过验证，要么重新输入，要么点击注册
                ctx.response.status = 400;
                ctx.response.body = {msg: '操作失败，请于管理员联系或稍后重试'};
            }
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '操作失败，请于管理员联系或稍后重试'};
        });
    })
    .delete('/delete',async(ctx)=> {
        let id = Number.parseInt(ctx.request.query.id);
        await User.destroy({
                'where':{'id':id}
            }).then(data => {
            if (data) {
                // 用户名存在通过验证
                ctx.response.status = 200;
                ctx.response.body = { msg: '操作成功'};
            } else {
                // 用户名或者密码错误没有通过验证，要么重新输入，要么点击注册
                ctx.response.status = 400;
                ctx.response.body = {msg: '操作失败，请于管理员联系或稍后重试'};
            }
        }).catch(err => {
            // 查找数据库发生错误，或者一些
            console.log(err);
            ctx.response.status = 400;
            ctx.response.body = {msg: '操作失败，请于管理员联系或稍后重试'};
        });
    });
module.exports = router;
