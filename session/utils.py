from datetime import datetime
import pytz

def get_user_timezone(request):
    tz_name = request.headers.get('Timezone') or request.query_params.get('timezone') or 'Asia/Kolkata'
    try:
        return pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        return pytz.timezone('Asia/Kolkata')




def convert_time_to_user_timezone(date, time_value, user_tz_str):
    if not date or not time_value:
        return None

    ist = pytz.timezone("Asia/Kolkata")
    user_tz = pytz.timezone(user_tz_str)

    standard_dt = ist.localize(datetime.combine(date, time_value))
  
    dt_user = standard_dt.astimezone(user_tz)
    return dt_user.strftime("%I:%M %p")


def format_user_time(t):
    if isinstance(t, str):
        try:
            t = datetime.strptime(t, "%H:%M:%S").time()
        except ValueError:
            return t  
    return t.strftime("%I:%M %p")