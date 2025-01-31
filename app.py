from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# Function to calculate fixed deposit
def calculate_fixed_deposit(principal, rate, time):
    try:
        return round(principal + (principal * rate * time) / 100, 2)  # Ensure it returns a rounded value
    except Exception as e:
        return str(e)

def calculate_sip(investment, tenure, interest, amount=0.0, is_year=True, is_percent=True, show_amount_list=False):
    tenure = tenure * 12 if is_year else tenure
    interest = interest / 100 if is_percent else interest
    interest /= 12
    amount_every_month = {}
    total_amount = investment * tenure

    for month in range(tenure):
        amount = (amount + investment) * (1 + interest)
        if show_amount_list:
            amount_every_month[month + 1] = amount  

    if show_amount_list:
        return {
            "Amount at Maturity": round(amount, 2),
            "Amount Every Month": {month: round(amount, 2) for month, amount in amount_every_month.items()},
        }
    else:
        return { "Amount at Maturity": round(amount, 2), "Total Investment": round(total_amount, 2) }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/FD.html', methods=['GET', 'POST'])
def fd():
    return render_template('FD.html')

@app.route('/FD.html/Result_FD.html', methods=['GET', 'POST'])
def calculate_fd():
    if request.method == 'POST':
        principle = float(request.form['Amount'])
        rate = int(request.form['Interest'])
        time = int(request.form['Years'])
        result = calculate_fixed_deposit(principle, rate, time)

        return render_template(
                               'Result_FD.html', 
                               principle=principle, 
                               rate=rate, 
                               time=time, 
                               result=result)
    return render_template('FD.html')

@app.route('/SIP.html', methods=['GET', 'POST'])
def sip():
    return render_template('SIP.html')

@app.route('/SIP.html/Result_SIP.html', methods=['GET', 'POST'])
def Result_SIP():
    if request.method == 'POST':
        investment = float(request.form['Investment'])
        tenure = int(request.form['tenure'])
        interest = int(request.form['Interest'])
        result_sip = calculate_sip(investment, tenure, interest)
        amount_at_maturity = result_sip["Amount at Maturity"]
        total_investment = result_sip["Total Investment"]
        return render_template(
            'Result_SIP.html',
            Investment=investment,
            tenure=tenure,
            interest=interest,
            amount_at_maturity=amount_at_maturity,
            total_investment=total_investment
        )
    return render_template('SIP.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
