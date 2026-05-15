module.exports = {
  authenticate: (req, res, next) => {
    // Placeholder auth middleware
    req.user = { id: 1, restaurant_id: 1, role: 'admin' };
    next();
  },
  authorize: (...roles) => {
    return (req, res, next) => {
      // Placeholder authorize
      next();
    }
  }
};
