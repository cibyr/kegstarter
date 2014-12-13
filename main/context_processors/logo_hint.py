from datetime import datetime
from django.db.models import Q
from ..models import LogoHint


def get_hints(request):
    now = datetime.now().date()
    hints = LogoHint.objects.filter(date__month=now.month, date__day=now.day).\
        exclude(~Q(date__year=now.year), use_year=True)
    return {'get_hints': hints,}
