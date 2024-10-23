from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import TaskStatus


def send_email_mock(to_email: str, task_title: str, new_status: str):
    import ipdb;ipdb.set_trace(context=20)
    from_email = "your-email@example.com"
    subject = f"Task '{task_title}' status changed"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    body = f"The status of the task '{task_title}' has been updated to '{new_status}'."
    msg.attach(MIMEText(body, 'plain'))

    print(f"Sending email to {to_email} with subject: {subject}")
    print(f"Body: {body}")


def on_task_status_change(task):
    if task.status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]:
        responsible_person_email = task.owner.email
        send_email_mock(responsible_person_email, task.title, task.status)
