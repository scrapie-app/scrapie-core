from fastapi import HTTPException, Depends, APIRouter, status


def projects_route_factory():
    router = APIRouter()

    @router.post('/create')
    def create_project():
        pass

    @router.get('/detail')
    def get_project_details():
        pass

    @router.get('/all')
    def get_all_projects():
        pass

    @router.post('/delete')
    def delete_project():
        pass

    @router.put('/api_key/associate')
    def associate_api_key_for_project():
        pass

    return router