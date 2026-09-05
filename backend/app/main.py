from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.routes import router

app=FastAPI(title='SkillSensei API',version='0.1.0',description='Career navigation API for SkillSensei')
app.add_middleware(CORSMiddleware,allow_origins=[settings.frontend_origin,'http://localhost:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(router,prefix='/api')

@app.get('/')
def root(): return {'name':'SkillSensei API','status':'running','docs':'/docs'}
