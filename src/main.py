import uvicorn
import os
import os.path
from logs import LOGGER
import pandas as pd
from io import StringIO
from fastapi import FastAPI, File, UploadFile, Form
from starlette.middleware.cors import CORSMiddleware
from logs import LOGGER
from service.am_service import amService
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")
ams = amService()


@app.get('/am/newest10')
async def count_text():
    try:
        return ams.get_newest_10_from_am()
    except Exception as e:
        LOGGER.error(e)
        return {'success': False, 'msg': e}


@app.post('/am/upload')
def load_text(file: UploadFile):
    try:
        content = file.file.read()
        content_str = str(content, encoding="utf-8")
        res = ams.import_am_data(content_str)
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'success': False, 'msg': e}


@app.get('/am')
def search_by_company_name(company_name: str):
    try:
        res = ams.get_am_by_company_name(company_name)
        if (len(res) == 0):
            return {'success': False, 'msg': 'no match company!'}
        else:
            return {'success': True, 'data': res}
    except Exception as e:
        LOGGER.error(e)
        return {'success': False, 'msg': e}


@app.get('/am/recommend/base_description')
def recommend_by_description(company_description: str):
    try:
        res = ams.recommend_by_description(company_description)
        if (len(res) == 0):
            return {'success': False, 'msg': 'no match company!'}
        else:
            return {'success': True, 'data': res}
    except Exception as e:
        LOGGER.error(e)
        return {'success': False, 'msg': e}


@app.get('/am/recommend/base_id')
def recommend_by_company_id(company_id: str):
    try:
        res = ams.recommend_by_company_id(company_id)
        if (len(res) == 0):
            return {'success': False, 'msg': 'no match company!'}
        else:
            return {'success': True, 'data': res}
    except Exception as e:
        LOGGER.error(e)
        return {'success': False, 'msg': e}


@app.get('/capability/all')
def get_all_capability():
    return ams.get_all_capability()


@app.post('/am/report')
def report_am(name: str = Form(), website: str = Form("nan"), address: str = Form("nan"), interest: str = Form("nan"),
              product: str = Form("nan"), project=Form("nan"), description: str = Form("nan"), capability: str = Form()):
    try:
        companyId=ams.insert_am_and_capabilities(name, website, address, interest,
                                       product, project, description, capability)
        return {'success': True, 'companyId': companyId}
    except Exception as e:
        return {'success': False, 'msg': e}


if __name__ == "__main__":
	#local
    uvicorn.run(app=app, host='127.0.0.1', port=5000)

	#home
    #uvicorn.run(app=app, host='172.20.10.5', port=5000)

	#lobby
    #uvicorn.run(app=app, host='172.16.1.253', port=5000)	
