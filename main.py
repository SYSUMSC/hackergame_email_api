import ssl
import logging  # 导入 logging 模块
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import aiosmtplib
from email.message import EmailMessage

app = FastAPI()

# 配置日志记录
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 配置 SMTP 服务器信息
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 465
SMTP_USER = "your_email@example.com"
SMTP_PASSWORD = "your_password"
SECRET_KEY = "your_secret_key"

class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    ip: str

@app.post("/send_email")
async def send_email(request: Request, email_request: EmailRequest, authorization: str = Header(None)):
    # 验证 Authorization 头部
    if authorization != f"Bearer {SECRET_KEY}":
        logging.warning(f"Unauthorized access attempt with token: {authorization}")
        raise HTTPException(status_code=401, detail="Unauthorized")

    logging.info(f"Received email request: To={email_request.to}, Subject={email_request.subject}, From IP={email_request.ip}")

    # 创建邮件
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = email_request.to
    message["Subject"] = email_request.subject
    message.set_content(email_request.body)

    # 手动指定 CA 证书路径
    context = ssl.create_default_context(cafile="/etc/ssl/certs/ca-certificates.crt")

    # 发送邮件
    try:
        if SMTP_PORT == 465:
            await aiosmtplib.send(
                message,
                hostname=SMTP_HOST,
                port=SMTP_PORT,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
                use_tls=True,
                tls_context=context  # 指定证书上下文
            )
        elif SMTP_PORT == 587:
            await aiosmtplib.send(
                message,
                hostname=SMTP_HOST,
                port=SMTP_PORT,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
                tls_context=context  # 指定证书上下文
            )
        elif SMTP_PORT == 25:
            await aiosmtplib.send(
                message,
                hostname=SMTP_HOST,
                port=SMTP_PORT,
                username=SMTP_USER,
                password=SMTP_PASSWORD,
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported SMTP port")

        logging.info(f"Email successfully sent to {email_request.to}")
        return {"success": True, "msg": "邮件发送成功"}
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return {"success": False, "msg": str(e)}

if __name__ == "__main__":
    import uvicorn
    logging.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
