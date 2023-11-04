from twilio.rest import Client

# Twilio 계정 SID 및 토큰
account_sid = 'ACd3b2f3867f2439e9d9ba28c8ca6ba1de'
auth_token = 'de7114c6bcedd639dacfc844182d610b'

# Twilio 클라이언트 생성
client = Client(account_sid, auth_token)

# SMS 보내기
def send_sms(msg):
    message = client.messages.create(
        body=msg,
        from_='+18482359453',  # Twilio에서 생성한 전화번호
        to='+8201071912644'      # 수신자 전화번호
    )
    
    print('SMS 전송 완료:', message.sid)