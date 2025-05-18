from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'  # Necesario para usar flash()

# Configuración de conexión PostgreSQL
DB_HOST = "localhost"
DB_NAME = "postgres"         # Confirmado por vos
DB_USER = "postgres"         # Confirmado por vos
DB_PASSWORD = "N1C0L45M0N74N4R1i$"  # Reemplazá esto por tu contraseña real

@app.route('/')
def login_form():
    return render_template('loginEncargado.html')

@app.route('/loginEncargado', methods=['POST'])
def login():
    
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    

    print(f"[DEBUG] Email ingresado: '{email}'")
    print(f"[DEBUG] Password ingresado: '{password}'")

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Consultamos primero solo por email para ver qué devuelve
        cursor.execute("SELECT * FROM Encargado WHERE email = %s", (email,))
        usuario_por_email = cursor.fetchone()
        print(f"[DEBUG] Usuario encontrado por email: {usuario_por_email}")
        
        if usuario_por_email:
            # Si existe el email, veamos qué contraseña tiene almacenada
            password_almacenada = usuario_por_email[4] if len(usuario_por_email) > 4 else None

            print(f"[DEBUG] Contraseña almacenada: '{password_almacenada}'")
            print(f"[DEBUG] ¿Coinciden contraseñas?: {password == password_almacenada}")
            
            # Ahora verificamos con la consulta original
            query = "SELECT * FROM Encargado WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            encargado = cursor.fetchone()
            print(f"[DEBUG] Resultado final de la consulta: {encargado}")
            
            if encargado:
                nombre = encargado[1]
                apellido = encargado[2]
                return f"Bienvenido {nombre} {apellido}!"
            else:
                flash("Contraseña incorrecta.")
                return redirect(url_for('login_form'))
        else:
            flash("El email no existe en nuestra base de datos.")
            return redirect(url_for('login_form'))

    except Exception as e:
        print(f"[ERROR] Fallo de conexión o consulta: {e}")
        flash("Error en el servidor al conectar con la base de datos.")
        return redirect(url_for('login_form'))
    finally:
        if 'conn' in locals():
            conn.close()
if __name__ == '__main__':
    app.run(debug=True)
