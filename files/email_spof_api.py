
import smtplib
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sender = "your@gmail.com"
password = "app password"
app = Flask(__name__)

@app.route('/send', methods=["GET"])
def send():   
    try:
        
        email = request.args.get("email")
        msg = MIMEMultipart()
        msg["From"] = f"Email Verification {sender}"
        msg["To"] = email
        msg["Subject"] ="Email Verificaton"

        msg.attach(MIMEText("ITS TEST EMAIL", "plain"))
        smtp_server = "smtp.gmail.com"
        port = 000

        with smtplib.SMTP(smtp_server,port) as server:
            server.starttls()
            server.login(sender,password)
            server.sendmail(sender, email, msg.as_string())
            server.quit()
            return jsonify({"text":f"Message send successfull to {email}"})
        
    except Exception as e:
        return jsonify({"Error":f"{e}"})   
    

if __name__ == '__main__':
    app.run(debug=True)
