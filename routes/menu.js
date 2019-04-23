require('dotenv').load();
require('dotenv').config();

const Router = require('koa-router');
const router = new Router();
const db = require('../db');
const {User,Role,Menu} = require('../models/sysmgr');
let sha1 = require('sha1'); //加密
const Sequelize = require('sequelize')
router
  .post('/getUserMenu',async(ctx,next)=> {
    await Menu.findAll({
      attributes: ['id',['name','menuname'],'url','descript',[Sequelize.col('roles.id'),'role_id'],[Sequelize.col('roles.name'),'rolename'],[Sequelize.col('roles->users.username'),'username'],[Sequelize.col('roles->users.id'),'user_id']],
      include: [{
        model: Role,
        attributes: [],
        include:[{
          model: User,
          attributes: [],
          where: {username: ctx.state.username},
        }],
      }],
    }).then(menus => {
      if (menus) {
        // 用户名存在通过验证
        ctx.response.status = 200;
        ctx.response.body = {menus: menus,msg: '请求成功'};
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
