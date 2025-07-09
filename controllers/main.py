# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

import logging
import os
import requests
import urllib.parse

from werkzeug.utils import redirect 
from jose import jwt  # pip install python-jose
from dotenv import load_dotenv

_logger = logging.getLogger(__name__)

# Auth0 Configuration
load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI")


class Auth0LoginController(http.Controller):

    @http.route('/auth0/login', type='http', auth='public', website=True)
    def auth0_login(self, provider=None, **kw):
        """Redirect user to Auth0 authorization endpoint for a specific provider."""
        params = {
            'response_type': 'code',
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'scope': 'openid profile email',
        }
        if provider:
            params['connection'] = provider  # e.g., google-oauth2, github

        url = f"https://{AUTH0_DOMAIN}/authorize?" + urllib.parse.urlencode(params)
        _logger.warning(f"🔁 Redirecting to: {url}")
        return redirect(url)


    @http.route('/auth0/callback', type='http', auth='public', website=True)
    def auth0_callback(self, **kw):
        _logger.info("⚡ Callback received with parameters: %s", kw)

        code = kw.get('code')
        if not code:
            _logger.error("❌ No authorization code in callback.")
            return redirect('/web/login')

        # Step 1: Exchange code for token
        token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI,
        }

        _logger.info("🔁 Exchanging code for tokens at: %s", token_url)
        try:
            token_http_response = requests.post(token_url, json=token_data)
            token_http_response.raise_for_status()
            token_response = token_http_response.json()
            _logger.info("✅ Token response received: %s", token_response)
        except Exception as e:
            _logger.exception("❌ Failed to exchange code for tokens.")
            return redirect('/web/login')

        id_token = token_response.get('id_token')
        if not id_token:
            _logger.error("❌ No ID token in response.")
            return redirect('/web/login')

        # Step 2: Decode token (unsafe for prod — verify signature in real use)
        try:
            user_info = jwt.decode(id_token, key='', options={
                "verify_signature": False,
                "verify_aud" : False
            })
            _logger.info("🔓 Decoded user info: %s", user_info)
        except Exception:
            _logger.exception("❌ Failed to decode ID token.")
            return redirect('/web/login')

        email = user_info.get('email')
        name = user_info.get('name') or email
        if not email:
            _logger.error("❌ Email missing from token.")
            return redirect('/web/login')

        # Step 3: Find or create Odoo user
        try:
            user_model = request.env['res.users'].sudo()
            user = user_model.search([('login', '=', email)], limit=1)
            if not user:
                _logger.info("👤 Creating new user: %s", email)
                user = user_model.create({
                    'name': name,
                    'login': email,
                    'email': email,
                    'groups_id': [(6, 0, [request.env.ref('base.group_user').id])],
                })
            else:
                _logger.info("🔎 Found existing user: %s", user.login)
        except Exception:
            _logger.exception("❌ Error during user lookup or creation.")
            return redirect('/web/login')

        # Step 4: Log user in
        try:
            sid = request.session.sid
            request.session.uid = user.id
            request.session.login = user.login
            request.session.session_token = user._compute_session_token(sid)
            _logger.info("✅ Successfully logged in user: %s (ID %s)", user.login, user.id)
        except Exception:
            _logger.exception("❌ Failed to set session for user.")
            return redirect('/web/login')


        return redirect('/web')