from django import template

register = template.Library()


@register.filter(name="calculate_pct")
def calculate_pct(completed_count, total_count):
    """
    درصد کارهای انجام شده را حساب می‌کند.
    استفاده در قالب: {{ completed_tasks|calculate_pct:all_tasks }}
    """
    try:
        total = int(total_count)
        completed = int(completed_count)

        if total > 0:
            return int((completed / total) * 100)
        return 0
    except (ValueError, TypeError):
        return 0
