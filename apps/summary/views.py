from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView

from configures.models import Configures
from debugtalks.models import DebugTalks
from envs.models import Envs
from interfaces.models import Interfaces
from projects.models import Projects
from reports.models import Reports
from testcases.models import Testcases
from testsuits.models import Testsuits
from rest_framework.response import Response


class SummaryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        user_info = {
            'username': user.username,
            'role':  '管理员' if user.is_superuser else '普通用户',
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else '',
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '',
        }

        projects_count = Projects.objects.all().count()
        interfaces_count = Interfaces.objects.all().count()
        testcases_count = Testcases.objects.all().count()
        testsuits_count = Testsuits.objects.all().count()
        configures_count = Configures.objects.all().count()
        envs_count = Envs.objects.all().count()
        debug_talks_count = DebugTalks.objects.all().count()
        reports_count = Reports.objects.all().count()
        ran_testcase_success = Reports.objects.aggregate(Sum('success'))['success__sum']
        ran_testcase_total = Reports.objects.aggregate(Sum('count'))['count__sum']
        if ran_testcase_total != 0:
            success_rate = int((ran_testcase_success / ran_testcase_total)*100)
            fail_rate = 100 - success_rate
        else:
            success_rate = 0
            fail_rate = 0

        statics = {
            'projects_count': projects_count,
            'interfaces_count': interfaces_count,
            'testcases_count': testcases_count,
            'testsuits_count': testsuits_count,
            'configures_count': configures_count,
            'envs_count': envs_count,
            'debug_talks_count': debug_talks_count,
            'reports_count': reports_count,
            'success_rate': success_rate,
            'fail_rate': fail_rate,
        }

        return Response(data={
            'user': user_info,
            'statistics': statics
        })