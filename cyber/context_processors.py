from .models import User

def global_context(request):
    
    # To display users according to their points in the employee cyber league table
    users = User.objects.exclude(is_superuser=True)
    table_users = users.order_by("-points").all()
    
    return {
        "table_users": table_users    
    }