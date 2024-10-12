from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import aiosmtplib
from email.message import EmailMessage

app = FastAPI()

# 配置 SMTP 服务器信息
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
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
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 创建邮件
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = email_request.to
    message["Subject"] = email_request.subject
    message.set_content(email_request.body)

    # 发送邮件
    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            use_tls=True,
        )
        return {"success": True, "msg": "邮件发送成功"}
    except Exception as e:
        return {"success": False, "msg": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)