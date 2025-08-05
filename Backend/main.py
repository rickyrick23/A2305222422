from routes.forms import FormData
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from forms import Form, submit_form, get_form_by_user_id, get_all_forms, update_form_by_user_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/form/submit")
async def handle_form_submission(form_data: Form):
    existing_forms = get_form_by_user_id(form_data.user_id)
    if existing_forms:
        return JSONResponse(
            status_code=400,
            content={"message": "Form already submitted for this user_id"}
        )
    submit_form(form_data)
    return {"message": "Form submitted successfully"}

@app.put("/form/submit")
async def update_form_submission(form_data: Form):
    updated = update_form_by_user_id(form_data.user_id, form_data)
    if updated:
        return {"message": "Form updated successfully"}
    return JSONResponse(
        status_code=404,
        content={"message": "No existing form found for this user_id"}
    )

@app.get("/form/get/{user_id}")
async def get_form(user_id: str):
    form = get_form_by_user_id(user_id)
    if not form:
        return JSONResponse(status_code=404, content={"message": "Form not found"})
    return form

@app.get("/form/all")
async def get_all():
    return get_all_forms()
