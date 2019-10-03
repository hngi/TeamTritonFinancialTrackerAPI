const crypto = require('crypto');

const generateSignupKey = () => {
	const buf = crypto.randomBytes(24);
	const created = Date.now();

	return {
		key: buf.toString('hex'),
		ts: created,
		exp: created + 86400000 //expiration of a day
	};
};

module.exports = { generateSignupKey };