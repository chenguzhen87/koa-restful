const db = require('../db');
const Sequelize = require('sequelize')
const moment = require('moment');

const LoginLog = db.sequelize.define('login_log', {
    id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    user_name: Sequelize.STRING(64),
    ip: Sequelize.STRING(64),
    descript: Sequelize.STRING(128),
    created: {
        type: Sequelize.DATE,
        defaultValue: Sequelize.NOW,
        get(){
            return moment(this.getDataValue('created')).format('YYYY-MM-DD HH:mm:ss');
        }
    },
});
module.exports = {
    LoginLog,
};
