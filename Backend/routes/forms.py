from pydantic import BaseModel
from typing import Optional
import shortuuid

class Form(BaseModel):
    id: Optional[str]
    name: str
    email: str
    age: int
    feedback: str
    user_id: str

submitted_forms = []

def submit_form(form_data: Form):
    form_data.id = shortuuid.uuid()
    submitted_forms.append(form_data)
    return form_data

def get_form_by_user_id(user_id: str):
    return [form for form in submitted_forms if form.user_id == user_id]

def get_all_forms():
    return submitted_forms

def update_form_by_user_id(user_id: str, updated_data: Form):
    for i, form in enumerate(submitted_forms):
        if form.user_id == user_id:
            updated_data.id = form.id
            submitted_forms[i] = updated_data
            return updated_data
    return None
