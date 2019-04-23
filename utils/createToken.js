const jwt = require('jsonwebtoken')
module.exports = function (user_name) {
    let expiry = new Date();
    expiry.setDate(expiry.getDate() + 7);//有效期设置为七天
    return jwt.sign({
        user_name: user_name,
        exp: parseInt(expiry.getTime() / 1000)//除以1000以后表示的是秒数 到期时间
    }, process.env.JWT_SECRET);
};
