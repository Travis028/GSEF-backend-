const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Simple logging middleware
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();
});

// Root endpoint
app.get('/', (req, res) => {
    res.json({ 
        success: true, 
        message: 'Restaurant SaaS Platform API is running',
        endpoints: {
            health: '/health',
            orders: '/api/orders',
            menu: '/api/menu',
            tables: '/api/tables'
        }
    });
});

// Health endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Orders endpoint
app.get('/api/orders', (req, res) => {
    res.json({ 
        success: true, 
        data: [], 
        message: 'Orders endpoint working',
        count: 0
    });
});

// Menu endpoint
app.get('/api/menu', (req, res) => {
    res.json({ 
        success: true, 
        data: [], 
        message: 'Menu endpoint working',
        count: 0
    });
});

// Tables endpoint
app.get('/api/tables', (req, res) => {
    res.json({ 
        success: true, 
        data: [], 
        message: 'Tables endpoint working',
        count: 0
    });
});

// API info
app.get('/api', (req, res) => {
    res.json({
        name: 'Restaurant SaaS Platform API',
        version: '1.0.0',
        status: 'running',
        endpoints: ['/health', '/api/orders', '/api/menu', '/api/tables']
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ 
        success: false, 
        error: 'Endpoint not found',
        path: req.url
    });
});

app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('✅ Restaurant API Server Running');
    console.log('='.repeat(50));
    console.log(`📍 Port: ${PORT}`);
    console.log(`📍 Health: http://localhost:${PORT}/health`);
    console.log(`📍 API: http://localhost:${PORT}/api`);
    console.log(`📍 Orders: http://localhost:${PORT}/api/orders`);
    console.log(`📍 Menu: http://localhost:${PORT}/api/menu`);
    console.log(`📍 Tables: http://localhost:${PORT}/api/tables`);
    console.log('='.repeat(50));
});
