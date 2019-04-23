require('dotenv').load();
require('dotenv').config();

const Router = require('koa-router');
const router = new Router();
const db = require('../../db/index');
const {User,Role,Menu} = require('../../models/sysmgr');
const Sequelize = require('sequelize')
router
    .get('/getUserMenu',async(ctx,next)=> {
        await Menu.findAll({
            attributes: ['id', 'pid', 'name', 'url', 'icon', 'sort', 'descript', [Sequelize.col('roles.id'), 'role_id'], [Sequelize.col('roles.name'), 'role_name'], [Sequelize.col('roles->users.user_name'), 'user_name'], [Sequelize.col('roles->users.id'), 'user_id']],
            include: [{
                model: Role,
                attributes: [],
                include: [{
                    model: User,
                    attributes: [],
                    where: {user_name: ctx.state.user_name},
                }],
            }],
        }).then(menus => {
            if (menus) {
                // 用户名存在通过验证
                ctx.response.status = 200;
                ctx.response.body = {menus: menus, msg: '请求成功'};
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
        });
    });
module.exports = router;
