import resend

resend.api_key = "re_Ac2Vc6QM_N7MV3wypBppyj3DqKpaN1nsi"

def send_email(to: str, subject: str, content: str):
    try:
        resend.Emails.send({
            "from": "onboarding@donbro.in",
            "to": to,
            "subject": subject,
            "html": content
        })
    except Exception as e:
        print(f"Failed to send email: {e}")

def invite_email_content (first_name,token):
    return f"""
    <p>Welcome to QB CHAT, {first_name}!</p>
    <p><a href='domain.com/signup-verify?token={token}'>Verify Your Account</a></p>
    <img src='internal-image-url' alt='Please use the QBurst network to access this site.' />
    """

def forgot_pwd_email_content (token):
    return f"""
    <p>Reset your password by clicking the link below:</p>
    <p><a href='domain.com/reset-password?token={token}'>Reset Password</a></p>
    <img src='internal-image-url' alt='Please use the QBurst network to access this site.' />
    """