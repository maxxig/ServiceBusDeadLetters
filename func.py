import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(text, login, password, emails_to, priority = '4'):
    msg = EmailMessage()
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(login, password)
    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(text, 'html'))
    msg['Subject'] = 'ServiceBus deadletters'
    msg['X-Priority'] = priority
    msg['From'] = login
    msg['To'] = emails_to
    smtpObj.send_message(msg)
    smtpObj.close()
def get_deadletters_cnt(servicebus_mgmt_client):
    result = {}
    for topic_properties in servicebus_mgmt_client.list_topics():
        subs = servicebus_mgmt_client.list_subscriptions(topic_properties.name)
        for sub in subs:
            prop = servicebus_mgmt_client.get_subscription_runtime_properties(topic_properties.name, sub.name)
            if (prop.dead_letter_message_count > 0):
                print("Topic Name: " + topic_properties.name +", " + sub.name + ": total_message_count - " + str(prop.total_message_count) +
                    ", active_message_count:" + str(prop.active_message_count) +
                    ", dead_letter_message_count:" + str(prop.dead_letter_message_count)
                    )
                result[topic_properties.name] = {'Subscription': sub.name, 'dead_letters_count': prop.dead_letter_message_count}
    return result
def generate_html_table(data):
    html = '<table border="1"><tr><th>Topic</th><th>Subscription</th><th>DeadLetters</th></tr>'
    for k, value in data.items():
        html += f'<tr><td>{str(k)}</td><td>{value["Subscription"]}</td><td>{value["dead_letters_count"]}</td></tr>'
    html += '</table>'
    return html