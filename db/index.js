//mysql数据库连接

const mysql = require('mysql');
const Sequelize = require('sequelize');
const {MYSQL_CONFIG} = require('../config');

const POOL = mysql.createPool({
  host: MYSQL_CONFIG.host,
  port: MYSQL_CONFIG.port,
  user: MYSQL_CONFIG.user,
  password: MYSQL_CONFIG.password,
  database: MYSQL_CONFIG.database,
});
// 根据配置实例化seq
const sequelize = new Sequelize(MYSQL_CONFIG.database, MYSQL_CONFIG.user, MYSQL_CONFIG.password, {
  host: MYSQL_CONFIG.host,
  port: MYSQL_CONFIG.port,
  dialect: MYSQL_CONFIG.dialect,
  pool: MYSQL_CONFIG.pool,
  define: {
    // 不要添加时间戳属性 (updatedAt, createdAt)
    timestamps: false,
    // 不使用驼峰式命令规则，这样会在使用下划线分隔
    // 这样 updatedAt 的字段名会是 updated_at
    underscored: true,
    // 禁止修改表名. 默认情况下
    // sequelize会自动使用传入的模型名（define的第一个参数）做为表名
    // 如果你不想使用这种方式你需要进行以下设置
    freezeTableName: true,
  }
});

module.exports = {
  mysql: function( sql, values ) {
    return new Promise(( resolve, reject ) => {
      POOL.getConnection(function(err, connection) {
        if (err) {
          resolve( err )
        } else {
          connection.query(sql, values, ( err, data) => {
            if ( err ) {
              reject( err )
            } else {
              resolve( data )
            }
            connection.release()
          })
        }
      })
    });
  },
  sequelize: sequelize,
}
