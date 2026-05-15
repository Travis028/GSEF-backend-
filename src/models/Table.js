const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Table = sequelize.define('Table', {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true
    },
    table_number: {
        type: DataTypes.INTEGER,
        allowNull: false
    },
    seating_capacity: {
        type: DataTypes.INTEGER,
        defaultValue: 4
    },
    status: {
        type: DataTypes.ENUM('available', 'occupied', 'reserved', 'unavailable'),
        defaultValue: 'available'
    },
    current_order_id: DataTypes.UUID,
    qr_code: DataTypes.TEXT
}, {
    timestamps: true
});

module.exports = Table;
