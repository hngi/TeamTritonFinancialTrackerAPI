module.exports = {
	ROOT_URL:
		process.env.NODE_ENV === 'production'
			? {
					WEB: 'https://fierce-dusk-36076.herokuapp.com/',
					API: ''
				}
			: {
					WEB: 'http://localhost:3000',
					API: 'http://localhost:5000'
				}
};