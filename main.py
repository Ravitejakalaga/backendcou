# main.py
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from common.database import engine, create_db_and_tables
from auth_bl import auth_router
from auth_bl.routes.magicAuth import router as magic_auth_router

# Routers
from cou_admin.api.country_routes import router as country_router
from cou_admin.api.currency_routes import router as currency_router
from cou_user.api.user_routes import router as user_router
from cou_course.api.course_routes import router as course_router
from cou_course.api.coursecategory_routes import router as coursecategory_router
from cou_course.api.coursesubcategory_routes import router as coursesubcategory_router
from cou_student.api.student_routes import router as student_router
from cou_user.api.job_role_routes import router as job_role_router
from cou_user.api.skill_routes import router as skill_router
from cou_onboarding import onboarding_progress_router
from cou_mentor.api.mentor_routes import router as mentor_router
from cou_mentor.api.mentorship_plan import router as mentorship_plans_router
from cou_user.api.userCourse_routes import router as usercourse_router
from cou_mentor.api.mentor_consultation import router as mentor_consultation_router

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Import models to register metadata
    from cou_admin.models.country import Country
    from cou_user.models.user import User
    from cou_user.models.role import Role
    from cou_user.models.logintype import LoginType
    from cou_user.models.loginhistory import LoginHistory
    from cou_user.models.job_role import JobRole
    from cou_user.models.skill import Skill
    from cou_course.models.coursesubcategory import CourseSubcategory
    from cou_onboarding.models.onboarding_progress import OnboardingProgress
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    lifespan=lifespan,
    debug=True,
    title="Your API",
    description="Your API Description",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    return {"status": "Application is healthy"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:*",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "https://backendcou-3.onrender.com",
        "https://frontendcou-smoky.vercel.app/",
        "https://*.vercel.app",
        "https://cou-ip-bkend-dev.vercel.app",
        "https://backendcou-r4846xwah-projectcou.vercel.app",
        "https://dev.CloudOU.vercel.com",
        "https://frontend-ovltx2las-projectcou.vercel.app",
        "https://frontend-cou.vercel.app",
        "https://dev-cloudou-gtbnajf0f6cvd2ar.centralindia-01.azurewebsites.net",
        "http://dev-cloudou-gtbnajf0f6cvd2ar.centralindia-01.azurewebsites.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Register routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(country_router, prefix="/api/v1")
app.include_router(currency_router, prefix="/api/v1")
app.include_router(course_router, prefix="/api/v1")
app.include_router(coursecategory_router, prefix="/api/v1")
app.include_router(coursesubcategory_router, prefix="/api/v1")
app.include_router(job_role_router, prefix="/api/v1")
app.include_router(mentor_router, prefix="/api/v1")
app.include_router(onboarding_progress_router, prefix="/api/v1")
app.include_router(skill_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(usercourse_router, prefix="/api/v1")
app.include_router(student_router, prefix="/api/v1")
app.include_router(mentorship_plans_router, prefix="/api/v1")
app.include_router(mentor_consultation_router, prefix="/api/v1")
app.include_router(magic_auth_router, prefix="/api/v1/magic-auth")
# Debug print routes
print("\nRegistered routes:")
for route in app.routes:
    print(f"{route.path} [{', '.join(route.methods)}]")

if __name__ == "__main__":
    # Import uvicorn ONLY for local dev
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
