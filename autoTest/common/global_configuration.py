# from user.user_list.models import Account, UserRole
# from user.user_detail.models import UserDetail
# from project.project_list.models import ProjectList
# from project.project_detail.models import ProjectDetail
import time
import random


def global_variable(request):
#     account_queryset = Account.objects.filter(is_delete=0).all()
#     user_role_queryset = UserRole.objects.filter().all()
    return locals()


def global_id():
    """
    全局15位ID
    """
    work_id = int(str(round(time.time() * 1000) // 2) + str(random.randint(1, 99)).zfill(
        15 - len(str(round(time.time() * 1000) // 2))))
    return locals()
