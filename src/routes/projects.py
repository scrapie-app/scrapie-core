from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import models
from schema import user as UserSchema, project as ProjectSchema
from ..util import helper_fns
from datetime import datetime
from time import time
from constants import messages

def projects_route_factory(options):
    router = APIRouter()
    helper_fns_factory = helper_fns.create_helper_fns_factory(options)
    get_current_active_user = helper_fns_factory['get_current_active_user']

    @router.post('/create', response_model=ProjectSchema.Project)
    def create_project(project_data: ProjectSchema.ProjectData, current_user: UserSchema.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        if not current_user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=messages.UNAUTHORIZED_USER)
        db_api_data_for_user = db.query(models.APIQuota).filter(
            and_(
                models.APIQuota.user_id == current_user.id,
                models.APIQuota.id == project_data.api_key_id,
            )
        ).first()
        if not db_api_data_for_user: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.INVALID_API_KEY)
        db_projects_data = models.Projects(
            user_id=current_user.id,
            name=project_data.name,
            description=project_data.description,
            api_key_id=db_api_data_for_user.id,
            active=True,
            created_at=datetime.fromtimestamp(time()),
            updated_at=datetime.fromtimestamp(time()),
        )
        db.add(db_projects_data)
        db.commit()
        db.flush()
        return db_projects_data

    @router.get('/detail', response_model=ProjectSchema.Project)
    def get_project_details(project_id: ProjectSchema.ProjectID, current_user: UserSchema.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        if not current_user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=messages.UNAUTHORIZED_USER)
        db_user_project_data = db.query(models.Projects).filter(
            and_(
                models.Projects.id == project_id.id,
                models.Projects.active == True,
            )
        ).first()
        if not db_user_project_data:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=messages.PROJECT_NOT_FOUND)
        return db_user_project_data

    @router.get('/all', response_model=ProjectSchema.ProjectsData)
    def get_all_projects(current_user: UserSchema.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        if not current_user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=messages.UNAUTHORIZED_USER)
        db_user_projects_data = db.query(models.Projects).filter(
            and_(
                models.Projects.user_id == current_user.id,
                models.Projects.active == True,
            )
        ).all()
        if not db_user_projects_data:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=messages.PROJECTS_NOT_FOUND)
        projects_list_data = []
        for project_data in db_user_projects_data:
            projects_list_data.append(
                ProjectSchema.ProjectBase(
                    id=project_data.id,
                    user_id=project_data.user_id,
                    name=project_data.name,
                    description=project_data.description,
                    api_key_id=project_data.api_key_id,
                    active=project_data.active,
                    created_at=project_data.created_at,
                    updated_at=project_data.created_at,
                )
            )
        return ProjectSchema.ProjectsData(projects=projects_list_data)

    @router.post('/delete', response_model=ProjectSchema.Project)
    def delete_project(project_id: ProjectSchema.ProjectID, current_user: UserSchema.UserResponse = Depends(get_current_active_user), db: Session = Depends(options['get_db'])):
        if not current_user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=messages.UNAUTHORIZED_USER)
        db_user_project_data = db.query(models.Projects).filter(models.Projects.id == project_id.id).first()
        if not db_user_project_data:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=messages.PROJECT_NOT_FOUND)
        db_user_project_data.active = False
        db_user_project_data.updated_at = datetime.fromtimestamp(time())
        db.commit()
        return db_user_project_data

    return router
