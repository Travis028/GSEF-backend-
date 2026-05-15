const express = require('express');
const router = express.Router();
const { Order } = require('../models');
const { authenticate } = require('../middleware/auth');

router.get('/', authenticate, async (req, res) => {
    try {
        const orders = await Order.findAll({
            where: { restaurant_id: req.user.restaurant_id },
            order: [['createdAt', 'DESC']],
            limit: 100
        });
        res.json({ success: true, data: orders });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

router.post('/', authenticate, async (req, res) => {
    try {
        const order = await Order.create({
            ...req.body,
            restaurant_id: req.user.restaurant_id,
            waiter_id: req.user.id
        });
        res.status(201).json({ success: true, data: order });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

router.put('/:id/status', authenticate, async (req, res) => {
    try {
        const { status } = req.body;
        const order = await Order.findByPk(req.params.id);
        if (!order) {
            return res.status(404).json({ error: 'Order not found' });
        }
        order.status = status;
        await order.save();
        res.json({ success: true, data: order });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

router.get('/:id', authenticate, async (req, res) => {
    try {
        const order = await Order.findByPk(req.params.id);
        if (!order) {
            return res.status(404).json({ error: 'Order not found' });
        }
        res.json({ success: true, data: order });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
