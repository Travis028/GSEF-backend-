const express = require('express');
const router = express.Router();
const { MenuItem } = require('../models');
const { authenticate, authorize } = require('../middleware/auth');

// Get all menu items
router.get('/', authenticate, async (req, res) => {
    try {
        const items = await MenuItem.findAll({
            where: { restaurant_id: req.user.restaurant_id }
        });
        res.json({ success: true, data: items });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get available menu items
router.get('/available', authenticate, async (req, res) => {
    try {
        const items = await MenuItem.findAll({
            where: { 
                restaurant_id: req.user.restaurant_id,
                is_available: true 
            }
        });
        res.json({ success: true, data: items });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Create menu item (admin/manager only)
router.post('/', authenticate, authorize('admin', 'manager'), async (req, res) => {
    try {
        const item = await MenuItem.create({
            ...req.body,
            restaurant_id: req.user.restaurant_id
        });
        res.status(201).json({ success: true, data: item });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Update menu item
router.put('/:id', authenticate, authorize('admin', 'manager'), async (req, res) => {
    try {
        const item = await MenuItem.findByPk(req.params.id);
        if (!item) {
            return res.status(404).json({ error: 'Menu item not found' });
        }
        await item.update(req.body);
        res.json({ success: true, data: item });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Delete menu item
router.delete('/:id', authenticate, authorize('admin'), async (req, res) => {
    try {
        const item = await MenuItem.findByPk(req.params.id);
        if (!item) {
            return res.status(404).json({ error: 'Menu item not found' });
        }
        await item.destroy();
        res.json({ success: true, message: 'Menu item deleted' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
