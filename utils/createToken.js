const jwt = require('jsonwebtoken')
module.exports = function (username){
    let expiry = new Date();
    expiry.setDate(expiry.getDate()+7);//有效期设置为七天
    const token = jwt.sign({
      username:username,
        exp:parseInt(expiry.getTime()/1000)//除以1000以后表示的是秒数 到期时间
    },process.env.JWT_SECRET);
    return token;
  }
