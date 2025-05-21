from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client

app = FastAPI()

# Centraliza credenciales en variables globales (puedes usar variables de entorno en producción)


client = Client(ACCOUNT_SID, AUTH_TOKEN)

class Number(BaseModel):
    code: str 
    phone: str 

class VerifyData(BaseModel):
    code: str
    code_country: str
    phone: str 

@app.get("/")
async def root():
    return {"message": "API Prosetel - FastAPI & Twilio"}

@app.post("/register")
async def registrarse(number: Number):
    try:
        verification = client.verify \
            .v2 \
            .services(SERVICE_SID) \
            .verifications \
            .create(to=f"{number.code}{number.phone}", channel='sms')

        # Retorna mensaje simple y status 200
        return {"message": "verification_sent"}

    except Exception as e:
        # Loguear error en consola para debug
        print(f"Error enviando código: {e}")
        # Lanzar HTTPException con status 500 y mensaje genérico
        raise HTTPException(status_code=500, detail="Error enviando código de verificación")

@app.post("/verify")
async def verify(data: VerifyData):
    try:
        check = client.verify \
                .v2 \
                .services(SERVICE_SID) \
                .verification_checks \
                .create(to=f"{data.code_country}{data.phone}", code=data.code)

        if check.status == "approved":
            print("✅ Código verificado exitosamente")
            return {"verified": True}
        else:
            print("❌ Código incorrecto")
            return {"verified": False}

    except Exception as ex:
        print(f"❌ Error verificando el código: {ex}")
        raise HTTPException(status_code=500, detail="Error verificando el código")
