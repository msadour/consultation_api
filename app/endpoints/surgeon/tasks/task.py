from django_q.models import Schedule


def create_surgeon_task():
    Schedule.objects.create(
        func="math.copysign",
        hook="hooks.print_result",
        args="2,-2",
        schedule_type=Schedule.MINUTES,
    )
