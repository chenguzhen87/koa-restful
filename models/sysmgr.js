const db = require('../db');
const Sequelize = require('sequelize')
const moment = require('moment');

const User = db.sequelize.define('user', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  username: {type: Sequelize.STRING(64), unique: 'uk_username'},
  password: Sequelize.STRING(128),
  descript: Sequelize.STRING(128),
  created: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
    get(){
      return moment(this.getDataValue('created')).format('YYYY-MM-DD HH:mm:ss');
    }
  },
  modified: {
    type: Sequelize.DATE,
    defaultValue: Sequelize.NOW,
    get(){
      return moment(this.getDataValue('modified')).format('YYYY-MM-DD HH:mm:ss');
    }
  },
});
const Role = db.sequelize.define('role', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  name: {
    type: Sequelize.STRING(64),
    unique: 'uk_rolename',
  },
  descript: Sequelize.STRING(128),
  created: Sequelize.DATE,
  modified: Sequelize.DATE,
});
const UserRole = db.sequelize.define('user_role', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  user_id: Sequelize.INTEGER,
  role_id: Sequelize.INTEGER,
});

const Menu = db.sequelize.define('menu', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  pid: Sequelize.INTEGER,
  name: Sequelize.STRING(64),
  url: {
    type: Sequelize.STRING(64),
    unique: 'uk_menuname'
  },
  descript: Sequelize.STRING(64),
});
const RoleMenu = db.sequelize.define('role_menu', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  role_id: Sequelize.STRING,
  menu_id: Sequelize.STRING
});
User.belongsToMany(Role, { through: UserRole, foreignKey: 'user_id' })
Role.belongsToMany(User, { through: UserRole, foreignKey: 'role_id' })
Role.belongsToMany(Menu, { through: RoleMenu, foreignKey: 'role_id' })
Menu.belongsToMany(Role, { through: RoleMenu, foreignKey: 'menu_id' })
module.exports = {
  User,
  Role,
  UserRole,
  Menu,
  RoleMenu,
}
