from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

'''SHOW STUDENT'''
@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

'''SHOW ID'''
@router_v1.get('/students/{id}')
async def get_book(id: int, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.id == id).first()

'''ADD'''
@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newstudent = models.Student(fname=student['fname'], lname=student['lname'], id=student['id'], born=student['born'], gender=student['gender'])
    db.add(newstudent)
    db.commit()
    db.refresh(newstudent)
    response.status_code = 201
    return newstudent

'''UPDATE'''
@router_v1.patch('/students/{id}')
async def update_student(id: int, student: dict, db: Session = Depends(get_db)):
    updatestudent = db.query(models.Student).filter(models.Student.id == id).first()
    
    updatestudent.fname = student.get('fname', updatestudent.fname)
    updatestudent.lname = student.get('lname', updatestudent.lname)
    updatestudent.born = student.get('born', updatestudent.born)
    updatestudent.gender = student.get('gender', updatestudent.gender)
    db.commit()
    db.refresh(updatestudent)
    return updatestudent

'''DELETE'''
@router_v1.delete('/students/{id}')
async def delete_book(id: int, db: Session = Depends(get_db)):
    deletestudent = db.query(models.Student).filter(models.Student.id == id).first()
    db.delete(deletestudent)
    db.commit()
    return {"Student successfully deleted"}

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
