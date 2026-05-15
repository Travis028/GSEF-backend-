const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Restaurant = sequelize.define('Restaurant', {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true
    },
    name: {
        type: DataTypes.STRING,
        allowNull: false
    },
    email: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
    },
    phone: DataTypes.STRING,
    address: DataTypes.TEXT,
    currency: {
        type: DataTypes.STRING,
        defaultValue: 'KES'
    },
    tax_rate: {
        type: DataTypes.DECIMAL(5,2),
        defaultValue: 16.00
    }
}, {
    timestamps: true
});

module.exports = Restaurant;
