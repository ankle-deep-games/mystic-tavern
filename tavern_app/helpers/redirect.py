from django.shortcuts import redirect
from django.contrib import messages
from typing import List, Dict, Optional
from django.http import HttpRequest, HttpResponseRedirect


def check_redirect_criteria(request: HttpRequest, criteria: List[Dict[str, object]]) -> Optional[HttpResponseRedirect]:
    """
    Check and process redirect criteria including setting messages with specific types and tags.

    Args:
        request: HttpRequest object.
        criteria: List of dictionaries each representing a redirect criterion.

    Returns:
        HttpResponseRedirect if a criterion is met, otherwise None.
    """
    for criterion in criteria:
        if criterion['condition']:
            message_type = criterion.get('message_type', 'error')
            message = criterion.get('message', '')

            if message_type == 'error':
                messages.error(request, message, extra_tags="alert alert-danger")
            elif message_type == 'info':
                messages.info(request, message, extra_tags="alert alert-info")

            return redirect(criterion['redirect_url'])
    return None
