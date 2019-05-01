require('dotenv').load();
require('dotenv').config();

const Router = require('koa-router');
const router = new Router();
const {LoginLog} = require('../../models/monitor');
const Sequelize = require('sequelize');
const Op = Sequelize.Op;

router
    .get('/getPageList',async(ctx,next)=> {
        let current_page = Number.parseInt(ctx.request.query.current_page);
        let page_size = Number.parseInt(ctx.request.query.page_size);
        let user_name = ctx.request.query.user_name;
        let start_date = ctx.request.query.start_date;
        let end_date = ctx.request.query.end_date;
        let start_index = (current_page - 1) * page_size;
        let where = {
            created: {
                [Op.between]: [start_date,end_date]
            }
        };
        if(user_name !== ''){
            where["user_name"] = {[Op.substring]:user_name};
        }
        await LoginLog.findAndCountAll({
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
    });
module.exports = router;
