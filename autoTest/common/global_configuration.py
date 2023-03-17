from user.user_list.models import Account, UserRole
from user.user_detail.models import UserDetail
from project.project_list.models import ProjectList
from project.project_detail.models import ProjectDetail


def global_variable(request):
    account_queryset = Account.objects.filter(is_delete=0).all()
    user_role_queryset = UserRole.objects.filter().all()
    return locals()
