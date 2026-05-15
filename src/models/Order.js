const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Order = sequelize.define('Order', {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true
    },
    order_number: {
        type: DataTypes.INTEGER,
        autoIncrement: true
    },
    status: {
        type: DataTypes.ENUM('pending', 'preparing', 'ready', 'completed', 'cancelled'),
        defaultValue: 'pending'
    },
    type: {
        type: DataTypes.ENUM('dine_in', 'takeaway', 'delivery'),
        defaultValue: 'dine_in'
    },
    subtotal: DataTypes.DECIMAL(10,2),
    tax: DataTypes.DECIMAL(10,2),
    total: DataTypes.DECIMAL(10,2),
    customer_name: DataTypes.STRING,
    customer_phone: DataTypes.STRING,
    notes: DataTypes.TEXT
}, {
    timestamps: true
});

module.exports = Order;
