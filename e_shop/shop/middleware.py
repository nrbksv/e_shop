import time
from datetime import timedelta


class UserStatMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('user_stat'):
            request.session['user_stat'] = dict()
        user_stat = request.session.get('user_stat')

        if not user_stat.get('time_start'):
            user_stat['time_start'] = time.time()

        if not user_stat.get('path_count'):
            user_stat['path_count'] = []

        res=[]
        if request.path == '/accounts/statistics/':
            each_page = user_stat.get('each_page',[])
            pages_time = [v for page in each_page for k, v in page.items()]
            pages_path = [k for page in each_page for k, v in page.items()]

            time_on_page = []
            for i in range(len(pages_time)):
                if i + 1 < len(pages_time):
                    time_ = pages_time[i + 1] - pages_time[i]
                else:
                    time_ = time.time() - pages_time[i]
                time_ = timedelta(seconds=time_)
                time_on_page.append(str(time_))

            res = [{pages_path[i]: time_on_page[i]} for i in range(len(time_on_page)) ]

        total_time = time.time() - user_stat.get('time_start')
        user_stat['total_time'] = str(timedelta(seconds=total_time))
        user_stat['page_count'] = len(res)
        user_stat['pages_info'] = res
        request.session['user_stat'] = user_stat

        response = self.get_response(request)

        user_stat = request.session.get('user_stat')

        if response.status_code == 200:
            if not user_stat.get('each_page'):
                user_stat['each_page'] = []
            if len(user_stat.get('each_page')) != 0:
                if request.path in user_stat['each_page'][-1].keys():
                    pass
                else:
                    user_stat['each_page'].append({request.path: time.time()})
            else:
                user_stat['each_page'].append({request.path: time.time()})

        request.session['user_stat'] = user_stat

        return response





