from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

DB_NAME = "InvestmentDB"  
DB_USER = "root"
DB_PASSWORD = "Mahesh@12"
DB_HOST = "localhost"
DB_PORT = 3306

def get_db_connection():
    return pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT,
    cursorclass=pymysql.cursors.DictCursor,
    ssl={'ssl': {}}
)


def setup_database():
    connection = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    connection.commit()
    connection.close()

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS fixed_deposits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            principal FLOAT NOT NULL,
            rate FLOAT NOT NULL,
            time INT NOT NULL,
            result FLOAT
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS sips (
            id INT AUTO_INCREMENT PRIMARY KEY,
            investment FLOAT NOT NULL,
            tenure INT NOT NULL,
            interest FLOAT NOT NULL,
            maturity_amount FLOAT,
            total_investment FLOAT
        )""")
    connection.commit()
    connection.close()

setup_database()  

def calculate_fixed_deposit(principal, rate, time):
    interest = (principal * rate * time) / 100
    return round(principal + interest, 2)

def calculate_sip(investment, tenure, interest, is_year=True):
    tenure = tenure * 12 if is_year else tenure  # Convert years to months
    interest = (interest / 100) / 12  # Convert to monthly rate
    amount = 0
    for _ in range(tenure):
        amount = (amount + investment) * (1 + interest)
    return {
        "Amount at Maturity": round(amount, 2),
        "Total Investment": round(investment * tenure, 2),
    }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/FD.html', methods=['GET', 'POST'])
def fd():
    return render_template('FD.html')

@app.route('/FD.html/Result_FD.html', methods=['GET', 'POST'])
def Calculate_fd():
    if request.method == 'POST':
        try:
            principal = float(request.form['Amount'])
            rate = float(request.form['Interest'])
            time = int(request.form['Years'])
            result = calculate_fixed_deposit(principal, rate, time)        
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO fixed_deposits (principal, rate, time, result) VALUES (%s, %s, %s, %s)",
                    (principal, rate, time, result)
                )
            connection.commit()
            connection.close()
            
            return render_template('Result_FD.html', principal=principal, rate=rate, time=time, result=result)
        except (ValueError, pymysql.MySQLError) as e:
            return render_template('FD.html', error=str(e))
    return render_template('FD.html')

@app.route('/SIP.html', methods=['GET', 'POST'])
def sip():
    return render_template('SIP.html')

@app.route('/SIP.html/Result_SIP.html', methods=['GET', 'POST'])
def result_sip():
    if request.method == 'POST':
        try:
            investment = float(request.form['Investment'])
            tenure = int(request.form['tenure'])
            interest = float(request.form['Interest'])
            result_sip = calculate_sip(investment, tenure, interest)
            amount_at_maturity = result_sip["Amount at Maturity"]
            total_investment = result_sip["Total Investment"]
            
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO sips (investment, tenure, interest, maturity_amount, total_investment) VALUES (%s, %s, %s, %s, %s)",
                    (investment, tenure, interest, amount_at_maturity, total_investment)
                )
            connection.commit()
            connection.close()
            
            return render_template('Result_SIP.html', Investment=investment, tenure=tenure, interest=interest, amount_at_maturity=amount_at_maturity, total_investment=total_investment)
        except (ValueError, pymysql.MySQLError) as e:
            return render_template('SIP.html', error=str(e))
    return render_template('SIP.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
