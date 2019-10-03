const jwt = require('jsonwebtoken');
const passport = require('passport');
const LocalStrategy = require('passport-local');
const JwtStrategy = require('passport-jwt').Strategy;
const { ExtractJwt } = require('passport-jwt');

require('dotenv').config();

const User = require('../models/user');
const secret = process.env.SECRET;

// Local Strategy
const localStrategy = new LocalStrategy(function(username, password, done) {
	// Use async function for awaiting promise in user.validPassword
	User.findOne({ username }, async function(err, user) {
		if (err) return done(err);
		if (!user) {
			return done(null, false);
		}
		if (!await user.validPassword(password)) {
			return done(null, false);
		}
		return done(null, user);
	});
});

const jwtOptions = {
	jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
	secretOrKey: secret
};

// Passport strategy for securing RESTful endpoints using JWT
const jwtStrategy = new JwtStrategy(jwtOptions, (payload, done) => {
	User.findById(payload.sub)
		.select('-password')
		.then((user) => {
			if (user) {
				done(null, user);
			} else {
				done(null, false);
			}
		})
		.catch((err) => {
			done(err, false);
		});
});





// passport global middleware
passport.use(localStrategy);
passport.use(jwtStrategy);

// passport local middleware
const passportOptions = { session: false };

const authenticate = passport.authenticate('local', passportOptions);
const restricted = passport.authenticate('jwt', passportOptions);

function makeToken(user) {
	const timestamp = new Date().getTime();
	const payload = {
		iss: 'Triton',
		sub: user._id,
		iat: timestamp
	};
	const options = {
		expiresIn: '7d'
	};
	return jwt.sign(payload, secret, options);
}


module.exports = {
	authenticate,
	restricted,
	makeToken,
};