# Odoo Auth0 Integration Module

This Odoo module provides seamless integration with [Auth0](https://auth0.com), enabling Single Sign-On (SSO) with multiple identity providers like Google and GitHub.

## 🌟 Features

- Secure authentication via Auth0
- Support for multiple providers (Google, GitHub, etc.)
- Automatic user provisioning in Odoo
- JWT decoding and validation
- Environment-based configuration for security

## 🚀 Getting Started

1. Clone this repo and place the module in your Odoo `addons` directory.
2. Create a `.env` file in the root of your project with the following keys:

```bash
AUTH0_DOMAIN=your-auth0-domain
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
AUTH0_REDIRECT_URI=http://localhost:8069/auth0/callback
```

3. Install the Python dependency:

```bash
pip install python-dotenv
```

4. Restart Odoo and activate the module.

## 🛡️ Security

Never commit your `.env` file. Always keep your secrets safe.

## 🧑‍💻 Author

Developed by Mohammad Hamdan with integration guidance from OpenAI's ChatGPT.
