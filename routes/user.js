require('dotenv').load();
require('dotenv').config();

const Router = require('koa-router');
const router = new Router();
const db = require('../db');
const {User} = require('../models/sysmgr');
const createToken = require('../utils/createToken');
let sha1 = require('sha1'); //加密

router
  .post('/login',async(ctx)=> {
    let username = ctx.request.body.username;
    let password = sha1(ctx.request.body.password);
    await User.findOne({
      where: {
        username: username,
        password: password
      }
    }).then(user => {
      if (user && (password === user.password)) {
        // 用户名存在通过验证
        ctx.response.status = 200;
        ctx.response.body = {user: user,token: createToken(username),msg: '请求成功'};
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
  })
  .post('/add',async(ctx)=> {
  await User.create({
    username: 'ttt',
    password: '123456',
    descript: 'test'
  }).then(data => {
    console.info(data)
    if (data) {
      // 用户名存在通过验证
      ctx.response.status = 200;
      ctx.response.body = {user: data,token: createToken(username),msg: '请求成功'};
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
