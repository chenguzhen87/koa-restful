// 验证token中间件
const jwt = require('jsonwebtoken');

module.exports = function (){
  return function * ( next ) {
    // 执行中间件的操作
    let ctx = this;
    if (ctx.url !== '/apis/user/login' && ctx.request.headers['authorization']) {
      let auth_attr = ctx.request.headers['authorization'].split(' ');
      if(auth_attr[0] !=='Bearer' || auth_attr.length !== 2) {
        ctx.response.body = {
          msg: '授权错误，请重新登陆'
        };
        ctx.response.status = 401;
      }else{
        let token = auth_attr[1];
        let decoded = jwt.decode(token, process.env.JWT_SECRET);
        // 如果过期了就重新登录
        if (token && decoded.exp <= Date.now() / 1000) {
          ctx.response.body = {
            msg: '授权已经过期，请重新登陆'
          };
          ctx.response.status = 401;
        }else{
          ctx.state.username = decoded.username;
        }
      }
    }
    yield next
  }
};
