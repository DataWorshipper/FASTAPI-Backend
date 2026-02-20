from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import  OAuth2PasswordRequestForm
from .. import database,schemas,model,utils,oauth2
router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(model.User).filter(model.User.email==user_credential.username).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credential")
    if not utils.verify(user_credential.password,user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credential")
     
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}

        
    
    
    
