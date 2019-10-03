/**
 * @swagger
 * definitions:
 *   User:
 *     type: object
 *     properties:
 *       first_name:
 *         type: string
 *       last_name:
 *         type: string
 *       email:
 *         type: string
 *       username:
 *         type: string
 *       password:
 *         type: string
 *         format: password
 *       phone:
 *         type: string
 *       required:
 *         - email
 *         - username
 *         - password
 *         - first_name
 *         - last_name
 */

const Joi = require('joi');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const saltRounds = 11;

/**
 * @swagger
 * definitions:
 *   User:
 *     type: object
 *     properties:
 *       first_name:
 *         type: string
 *       last_name:
 *         type: string
 *       email:
 *         type: string
 *       username:
 *         type: string
 *       password:
 *         type: string
 *         format: password
 *       phone:
 *         type: string
 *       required:
 *         - email
 *         - username
 *         - password
 *         - first_name
 *         - last_name
 */
const UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    minlength: 1,
    maxlength: 150
  },
  first_name: {
    type: String,
    required: true,
    minlength: 1,
    maxlength: 255
  },
  last_name: {
    type: String,
    required: true,
    minlength: 1,
    maxlength: 255
  },
  email: {
    type: String,
    required: true,
    minlength: 5,
    maxlength: 255,
    unique: true
  },
  phone: {
    type: String,
    minlength: 1,
    maxlength: 255,
  },
  password: {
    type: String,
    required: true,
    minlength: 1,
  },
});


// Hash passwords before saving to database
UserSchema.pre('save', function(next) {
	if (!this.isModified('password')) return next();
	bcrypt.hash(this.password, saltRounds, (err, hash) => {
		if (err) return next(err);
		this.password = hash;
		next();
	});
});

// Hash passwords on update
UserSchema.pre('update', function(next) {
	if (!this.isModified('password')) return next();
	bcrypt.hash(this.password, saltRounds, (err, hash) => {
		if (err) return next(err);
		this.password = hash;
		next();
	});
});

// Method to check user inputed password against hashed password
UserSchema.methods.validPassword = async function(passwordGuess) {
	try {
		return await bcrypt.compare(passwordGuess, this.password);
	} catch (err) {
		return err;
	}
};

UserSchema.methods.newPassword = async function(password) {
	try {
		return await bcrypt.hash(password, saltRounds);
	} catch (err) {
		return err;
	}
};

//function to validate user 
UserSchema.methods.validateUser = async function (user) {
  const schema = {
    name: Joi.string().min(3).max(50).required(),
    email: Joi.string().min(5).max(255).required().email(),
    password: Joi.string().min(3).max(255).required()
  };

  return Joi.validate(user, schema);
}

/**
 * @swagger
 * definitions:
 *   User:
 *     type: object
 *     properties:
 *       first_name:
 *         type: string
 *       last_name:
 *         type: string
 *       email:
 *         type: string
 *       username:
 *         type: string
 *       password:
 *         type: string
 *         format: password
 *       phone:
 *         type: string
 *       required:
 *         - email
 *         - username
 *         - password
 *         - first_name
 *         - last_name
 */

module.exports = mongoose.model('User', UserSchema);;