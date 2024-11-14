# htmlTemplates.py

signup_html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Sign Up</title>
  </head>
  <body>
    <h2>Sign Up</h2>
    <form method="POST">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" required>
      <br>
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required>
      <br>
      <button type="submit">Sign Up</button>
    </form>
  </body>
</html>
"""

login_html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Login</title>
  </head>
  <body>
    <h2>Login</h2>
    <form method="POST">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" required>
      <br>
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required>
      <br>
      <button type="submit">Login</button>
    </form>
  </body>
</html>
"""

main_html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Main Page</title>
  </head>
  <body>
    <h2>Welcome to the Main Page</h2>
    <p>This is the main page content where users can interact with the app.</p>
  </body>
</html>
"""

# Placeholder for existing templates
existing_template_html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Existing Template</title>
  </head>
  <body>
    <h2>Existing Template</h2>
    <p>This is a placeholder for existing functionality.</p>
  </body>
</html>
"""
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://t3.ftcdn.net/jpg/03/22/38/32/240_F_322383277_xcXz1I9vOFtdk7plhsRQyjODj08iNSwB.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/jpeg;base64,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">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

# Assigning the templates to respective variables
templates = {
    'signup': signup_html,
    'login': login_html,
    'main': main_html,
    'existing_template': existing_template_html,
    # Add your additional existing templates here...
}

def get_template(name):
    return templates.get(name, 'Template not found')
