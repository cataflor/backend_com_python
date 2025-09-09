from flask import Flask, render_template,  redirect, request, flash
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'caroline'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/admin')


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        #testar se é admin
        if username == 'admin' and password == 'admin':
            return render_template("admin.html")
        
        #Depois se é um usuário cadastrado
        with open('users.json', 'r') as users_file:
            users = json.load(users_file)
        
        cont = 0
        for user in users:               
            if user['username'] == username and user['password'] == password:
                return render_template("users.html")
            cont += 1

        # Se não for nenhum dos dois, retorna invalido
        if cont == len(users):
            flash('Invalid username or password')
            return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    user = []
    username = request.form.get('username')
    password = request.form.get('password')

    try: 
        with open('users.json', 'r') as users_file:
            users = json.load(users_file) 
            if not isinstance(users, list):
                users = users.get('users', [])
    except (FileNotFoundError, json.JSONDecodeError):
        users = []
    
    if any(user['username'] == username for user in users):
        flash('Username already exists.')
        return redirect('/register')
    
    user.append({
        "username": username,
        "password": password
    })
 
    newUser = users + user
    
    users.sort(key=lambda user: user['username'].lower())
    
    with open('users.json', 'w') as user_save:
        json.dump(newUser, user_save, indent=4, ensure_ascii=False)

    return render_template('admin.html')

if __name__ == '__main__':  
    app.run(debug=True)  