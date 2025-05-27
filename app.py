from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = 'data/database.db'

# ---------- DB Initialization ----------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        # Table for rules
        c.execute('''CREATE TABLE IF NOT EXISTS rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rule_name TEXT,
                        column_name TEXT,
                        value TEXT,
                        created_by TEXT,
                        created_date TEXT,
                        updated_by TEXT,
                        updated_date TEXT
                    )''')

        # Table for campaigns
        c.execute('''CREATE TABLE IF NOT EXISTS campaigns (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        campaign_name TEXT,
                        rule_name TEXT,
                        column_name TEXT,
                        created_by TEXT,
                        created_date TEXT,
                        updated_by TEXT,
                        updated_date TEXT
                    )''')

        conn.commit()


# ---------- Routes ----------
@app.route('/')
def login():
    return render_template('home.html')

@app.route('/rules', methods=['GET', 'POST'])
def rules():
    if request.method == 'POST':
        rule_name = request.form['rule_name']
        column_name = request.form['column_name']
        value = request.form['value']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO rules (rule_name, column_name, value, created_by, created_date) VALUES (?, ?, ?, ?, ?)",
                      (rule_name, column_name, value, 'admin', now))
            conn.commit()
        return redirect(url_for('rules'))

    return render_template('add_rules.html')

@app.route('/rules/table')
def rules_table():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM rules")
        rules_data = c.fetchall()
    return render_template('rules.html', rules=rules_data)

@app.route('/rules/edit/<int:id>', methods=['GET', 'POST'])
def edit_rule(id):
    if request.method == 'POST':
        rule_name = request.form['rule_name']
        column_name = request.form['column_name']
        value = request.form['value']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("UPDATE rules SET rule_name=?, column_name=?, value=?, updated_by=?, updated_date=? WHERE id=?",
                      (rule_name, column_name, value, 'admin', now, id))
            conn.commit()
        return redirect(url_for('rules_table'))

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM rules WHERE id=?", (id,))
        rule = c.fetchone()
    return render_template('edit_rules.html', rule=rule)

@app.route('/rules/delete/<int:id>')
def delete_rule(id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM rules WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('rules_table'))

# ---------- Campaign Routes ----------
@app.route('/campaign/', methods=['GET', 'POST'])
def campaign():
    if request.method == 'POST':
        rule_name = request.form['rule_name']
        campaign_name = request.form['campaign_name']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO campaigns (rule_name, campaign_name, created_by, created_date)",
                      (rule_name, campaign_name, 'admin', now))
            conn.commit()
        return redirect(url_for('campaign'))

    return render_template('add_campaign.html')

@app.route('/campaign/table')
def campaign_table():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM campaigns")
        campaigns = c.fetchall()
    return render_template('campaign.html', campaigns=campaigns)

@app.route('/campaign/edit/<int:id>', methods=['GET', 'POST'])
def edit_campaign(id):
    if request.method == 'POST':
        rule_name = request.form['rule_name']
        campaign_name = request.form['campaign_name']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("UPDATE campaigns SET rule_name=?, campaign_name=?, updated_by=?, updated_date=? WHERE id=?",
                      (rule_name, campaign_name, 'admin', now, id))
            conn.commit()
        return redirect(url_for('campaign'))

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM campaigns WHERE id=?", (id,))
        campaign = c.fetchone()
    return render_template('edit_campaign.html', campaign=campaign)

@app.route('/campaign/delete/<int:id>')
def delete_campaign(id):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM campaigns WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('campaign'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/campaigns')
def campaigns():
    return render_template('campaign.html')

@app.route('/add_rules')
def add_rules():
    return render_template('add_rules.html')

@app.route('/add_campaign')
def add_campaign():
    return render_template('add_campaign.html')

@app.route('/edit_rules')
def edit_rules():
    return render_template('edit_rules.html')

# ---------- Main ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
