from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "some-super-secret-fixed-key-123"
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

oauth = OAuth(app)

github = oauth.register(
    name='github',
    client_id='Ov23liooRsf6dC9XcIr9',
    client_secret='663417641dd97ae002ef0ac558a6c0109fbfde6a',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>GitHub OAuth Login</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background: #0d1117;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .card {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 40px;
                text-align: center;
                width: 340px;
            }
            .card h2 { color: #f0f6fc; margin-bottom: 10px; }
            .card p { color: #8b949e; margin-bottom: 24px; }
            .btn {
                display: inline-flex;
                align-items: center;
                gap: 10px;
                background: #238636;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                text-decoration: none;
                font-size: 15px;
                font-weight: bold;
                transition: background 0.2s;
            }
            .btn:hover { background: #2ea043; }
            svg { width: 20px; height: 20px; fill: white; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Welcome</h2>
            <p>Sign in with your GitHub account to continue.</p>
            <a href="/login" class="btn">
                <svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                    0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                    -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66
                    .07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15
                    -.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0
                    1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82
                    1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01
                    1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                </svg>
                Login with GitHub
            </a>
        </div>
    </body>
    </html>
    '''

@app.route('/login')
def login():
    return github.authorize_redirect(url_for('callback', _external=True))

@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    user = github.get('user').json()
    session['user'] = user
    return redirect('/profile')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/')
    
    user = session['user']
    name = user.get('name') or user.get('login', 'N/A')
    username = user.get('login', '')
    avatar = user.get('avatar_url', '')
    followers = user.get('followers', 0)
    following = user.get('following', 0)
    github_url = user.get('html_url', '')
    bio = user.get('bio') or 'No bio provided.'
    public_repos = user.get('public_repos', 0)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{username} — GitHub Profile</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: Arial, sans-serif;
                background: #0d1117;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }}
            .card {{
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 36px;
                text-align: center;
                width: 380px;
            }}
            .avatar {{
                width: 110px;
                height: 110px;
                border-radius: 50%;
                border: 3px solid #238636;
                margin-bottom: 16px;
            }}
            .name {{
                color: #f0f6fc;
                font-size: 22px;
                font-weight: bold;
            }}
            .username {{
                color: #8b949e;
                font-size: 15px;
                margin-bottom: 10px;
            }}
            .bio {{
                color: #c9d1d9;
                font-size: 14px;
                margin-bottom: 20px;
                font-style: italic;
            }}
            .stats {{
                display: flex;
                justify-content: center;
                gap: 24px;
                margin-bottom: 24px;
            }}
            .stat {{
                text-align: center;
            }}
            .stat-number {{
                color: #f0f6fc;
                font-size: 20px;
                font-weight: bold;
            }}
            .stat-label {{
                color: #8b949e;
                font-size: 12px;
            }}
            .divider {{
                border: none;
                border-top: 1px solid #30363d;
                margin: 20px 0;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                border-radius: 8px;
                text-decoration: none;
                font-size: 14px;
                font-weight: bold;
                margin: 6px;
                transition: background 0.2s;
            }}
            .btn-green {{
                background: #238636;
                color: white;
            }}
            .btn-green:hover {{ background: #2ea043; }}
            .btn-red {{
                background: #b62324;
                color: white;
            }}
            .btn-red:hover {{ background: #d1242f; }}
        </style>
    </head>
    <body>
        <div class="card">
            <img src="{avatar}" class="avatar" alt="avatar"/>
            <div class="name">{name}</div>
            <div class="username">@{username}</div>
            <div class="bio">{bio}</div>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{followers}</div>
                    <div class="stat-label">Followers</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{following}</div>
                    <div class="stat-label">Following</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{public_repos}</div>
                    <div class="stat-label">Repos</div>
                </div>
            </div>
            <hr class="divider"/>
            <a href="{github_url}" target="_blank" class="btn btn-green">View GitHub Profile</a>
            <a href="/logout" class="btn btn-red">Logout</a>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/api/secure-data')
def secure_data():
    if 'user' not in session:
        return {'error': 'Unauthorized'}, 401
    return {
        'message': 'You have access to secure data!',
        'user': session['user']['login'],
        'secret': 'TOP_SECRET_DATA_42'
    }

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')