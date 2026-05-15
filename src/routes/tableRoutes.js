const express = require('express');
const router = express.Router();
const { Table } = require('../models');
const { authenticate, authorize } = require('../middleware/auth');

// Get all tables
router.get('/', authenticate, async (req, res) => {
    try {
        const tables = await Table.findAll({
            where: { restaurant_id: req.user.restaurant_id },
            order: [['table_number', 'ASC']]
        });
        res.json({ success: true, data: tables });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Create table
router.post('/', authenticate, authorize('admin', 'manager'), async (req, res) => {
    try {
        const table = await Table.create({
            ...req.body,
            restaurant_id: req.user.restaurant_id
        });
        res.status(201).json({ success: true, data: table });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Update table status
router.patch('/:id/status', authenticate, async (req, res) => {
    try {
        const { status } = req.body;
        const table = await Table.findByPk(req.params.id);
        if (!table) {
            return res.status(404).json({ error: 'Table not found' });
        }
        table.status = status;
        await table.save();
        res.json({ success: true, data: table });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
