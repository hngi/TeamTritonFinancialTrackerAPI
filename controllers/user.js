const User = require('../models/user');
const { makeToken } = require('../middleware/passport');

// Register a user
 exports.signup = (req, res) => {
    const { username } = req.body;
	User.findOne({ username }).then((existingUser) => {
		// If user with that username exists
		if (existingUser) {
			// if user already signed up locally
			return res.status(403).json({ message: 'problem signing up' });
		} else {
			const user = new User(req.body);
			user
				.save()
				.then((user) => {
					const token = makeToken(user);
					res.status(201).json({ token });
				})
				.catch((err) => {
					res.status(500).json(err);
				});
		}
	});
};

// Login a user
exports.login = (req, res) => {
    const { _id, email, phone, first_name, last_name, username } = req.user
	if(!req.user) {
		return res.status(401);
	}
	res.status(200).json({ token: makeToken(req.user), user: { _id, email, phone, first_name, last_name, username } });
};